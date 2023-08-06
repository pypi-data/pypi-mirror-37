name = "pymortar"

import importlib
import pickle
import IPython
import grpc
import base64
import uuid
#import result
import pytz
import json
import pandas as pd
from pymortar import hod_pb2
from pymortar import mdal_pb2
from pymortar import mortar_pb2
from pymortar import mortar_pb2_grpc

import sqlite3
conn = sqlite3.connect('mortar.db')
conn.text_factory = str
# create tables
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS qualify (
    query TEXT,
    objectid TEXT,
    inserted TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
c.execute('''CREATE TABLE IF NOT EXISTS fetch (
    site TEXT,
    query TEXT,
    objectid TEXT,
    inserted TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
c.execute('''CREATE TABLE IF NOT EXISTS objects (
    object BLOB,
    objectid TEXT,
    inserted TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

import pyarrow.plasma as plasma

agg_funcs = {
    "RAW": mdal_pb2.RAW,
    "MEAN": mdal_pb2.MEAN,
    "MIN": mdal_pb2.MIN,
    "MAX": mdal_pb2.MAX,
    "COUNT": mdal_pb2.COUNT,
    "SUM": mdal_pb2.SUM,
}
def parse_agg_func(name):
    return mdal_pb2.AggFunc.Value(name.upper())

class cache:
    def __init__(self, plasmaclient, sqlconn):
        self.client = plasmaclient
        self.conn = sqlconn
        self.disk = self.conn.cursor()

    def put_disk(self, objectid_b64, objectbytes):
        self.disk.execute("INSERT INTO objects(objectid, object) VALUES (?, ?);", (objectid_b64, objectbytes))
        self.conn.commit()

    def get_disk(self, objectid_b64):
        objectid = plasma.ObjectID(base64.b64decode(objectid_b64))
        res = self.disk.execute("SELECT object FROM objects WHERE objectid=?", (objectid_b64,))
        buf = res.fetchone()
        pb = self.client.create(objectid, len(buf[0]))
        pd.np.copyto(pd.np.frombuffer(pb, dtype='uint8'), pd.np.frombuffer(buf[0],dtype='uint8'))
        self.client.seal(objectid)
        return self.client.get(objectid, timeout_ms=10000000)
        
    def put(self, obj):
        """
        Returns ObjectID
        """
        objectid = self.client.put(obj)
        b64hash = base64.b64encode(objectid.binary())
        buf = self.client.get_buffers([objectid])[0].to_pybytes()
        #IPython.embed()
        self.put_disk(b64hash, buf)
        return objectid

    def get(self, objectid):
        b64hash = base64.b64encode(objectid.binary())
        if self.client.contains(objectid):
            obj = self.client.get(objectid, timeout_ms=10000000) # 10 sec
            buf = self.client.get_buffers([objectid])[0].to_pybytes()
            #self.put_disk(b64hash, buf)
            return obj
        else:
            obj = self.get_disk(b64hash)
            #self.put_disk(b64hash, obj)
            return obj

    def getb64(self, b64hash):
        objectid = plasma.ObjectID(base64.b64decode(b64hash))
        return self.get(objectid)

class MortarClient:
    def __init__(self, caddr, with_cache=True):
        self.with_cache = with_cache
        self.client = plasma.connect("/tmp/plasma", "", 0)
        self.channel = grpc.insecure_channel(caddr, options=[
                  ('grpc.max_send_message_length', 100 * 1024 * 1024),
                  ('grpc.max_receive_message_length', 100 * 1024 * 1024)
        ])
        self.stub = mortar_pb2_grpc.MortarStub(self.channel)
        self.cache = cache(self.client, conn)

    def qualify(self, required):
        if self.with_cache:
            ro = c.execute("SELECT * FROM qualify WHERE query=?", (json.dumps(required),))
            ans = ro.fetchone()
            if ans:
                return self.cache.getb64(ans[1])

        q = [hod_pb2.QueryRequest(query=req) for req in required]
        sites = self.stub.Qualify(mortar_pb2.QualifyRequest(requiredqueries=q))

        objectid = self.cache.put(list(sites.sites))
        b64hash = base64.b64encode(objectid.binary())

        c.execute("INSERT INTO qualify(query, objectid) VALUES (?, ?);", (json.dumps(required), b64hash))
        conn.commit()

        return list(sites.sites)

    def fetch(self, sitename, request):

        if self.with_cache:
            ro = c.execute("SELECT objectid FROM fetch WHERE query=?", (sitename+json.dumps(request),))
            ans = ro.fetchone()
            if ans:
                objectid = plasma.ObjectID(base64.b64decode(ans[0]))
                return self.cache.get(objectid), objectid

        aggs = {}
        for varname, aggfunclist in request["Aggregation"].items():
            aggs[varname] = mdal_pb2.Aggregation(funcs=[parse_agg_func(func) for func in aggfunclist])
        #print aggs
        vardefs = {}
        for varname, defn in request["Variables"].items():
            vardefs[varname] = mdal_pb2.Variable(
                name = varname,
                definition = defn["Definition"] % sitename,
                units = defn.get("Units",None),
            )
        #print vardefs
        params = mdal_pb2.DataQueryRequest(
            composition = request["Composition"],
            aggregation = aggs,
            variables = vardefs,
            time = mdal_pb2.TimeParams(
                start = request["Time"]["Start"],
                end = request["Time"]["End"],
                window = request["Time"]["Window"],
                aligned = request["Time"]["Aligned"],
            ),
        )
        #print params
        tz = pytz.timezone("US/Pacific")
        resp = self.stub.Fetch(mortar_pb2.FetchRequest(request=params), timeout=120)
        if resp.error != "":
            raise Exception(resp.error)
        
        #IPython.embed()
        values = [x.value for x in resp.response.values]
        if pd.np.array(values).size > 0:
            t = resp.response.times
            v = pd.np.array(values)
            #if len(resp.response.times) > pd.np.array(values).shape[1]:
            df = pd.DataFrame.from_records(values).T
            df.columns = resp.response.uuids
            df.index = pd.to_datetime(resp.response.times)

            mapping = {}
            for k, v in resp.response.mapping.items():
                mapping[k] = [str(uuid.UUID(bytes=x)) for x in v.uuids]

            result = {
                'df': df,
                'sitename': sitename,
                'context': {x.uuid: dict(x.row) for x in resp.response.context},
                'mapping': mapping,
            }

            _objectid = self.cache.put(result)
            objectid = base64.b64encode(_objectid.binary())
            c.execute("INSERT INTO fetch(site, query, objectid) VALUES (?, ?, ?);", (sitename, sitename+json.dumps(request), objectid))
            conn.commit()
            return result,_objectid
        return None, None

    def RUN(self, qualify, fetch, clean=None, execute=None, aggregate=None, with_cache=True):
        print('FETCH:',fetch)
        print('CLEAN:',clean)
        print('EXECUTE:',execute)
        print('AGG:',aggregate)

        if qualify is None or not isinstance(qualify, str):
            raise Exception("QUALIFY must be string path of module")
        qualifyrun = importlib.import_module(qualify)

        if fetch is None or not isinstance(fetch, str):
            raise Exception("FETCH must be string path of module")
        fetchrun = importlib.import_module(fetch)

        if clean is not None:
            cleanrun = importlib.import_module(clean)
        else:
            cleanrun = None

        if execute is not None:
            executerun = importlib.import_module(execute)
        else:
            executerun = None

        if aggregate is not None:
            aggregaterun = importlib.import_module(aggregate)
        else:
            aggregaterun = None

        sites = qualifyrun.run(self)

        res = []
        retries_left = 100
        while retries_left > 0:
            try:
                for objid in fetchrun.run(self, sites=sites):
                    if cleanrun is not None:
                        objid2 = cleanrun.run(self, objid)
                    else:
                        objid2 = objid

                    if executerun is not None:
                        res.append(executerun.run(self, objid2))

                    if aggregaterun is None:
                        yield self.cache.get(objid2)
                
                if aggregaterun is not None:
                    yield aggregaterun(res)
            except Exception as e:
                print("RETRYINg:",e)
                retries_left -= 1
                continue
            break

        yield res


if __name__ == '__main__':
    m = MortarClient("localhost:9001")
    import pickle
    import pathlib
    import os
    cachefilename = "mycache.pickle"
    cachefile = pathlib.Path(cachefilename)
    if cachefile.is_file():
        sites = pickle.load(open(cachefilename, 'rb'))
    else:
        q = """SELECT ?temp ?temp_uuid WHERE {
               ?temp rdf:type/rdfs:subClassOf* brick:Temperature_Sensor .
               ?temp bf:uuid ?temp_uuid
               };""" 
        resp = m.qualify([q])
        sites = list(resp.sites)
        pickle.dump(sites, open(cachefilename, 'wb'))

    for s in sites:
        request = {
            "Composition": ["temp"],
            "Aggregation": {
                "temp": ["MEAN"],
            },
            "Variables": {
                "temp": {
                    "Definition": """SELECT ?temp ?temp_uuid FROM %s WHERE {
                        ?temp rdf:type/rdfs:subClassOf* brick:Temperature_Sensor .
                        ?temp bf:uuid ?temp_uuid
                    };""" % s,
                },
            },
            "Time": {
                "Start":  "2018-08-01T10:00:00-07:00",
                "End":  "2019-01-12T10:00:00-07:00",
                "Window": '1d',
                "Aligned": True,
            },
        }
        resp = m.fetch(request)
        #if len(resp) > 0:
        #    print(resp.describe())
        print(resp[resp.columns[0]].describe())
