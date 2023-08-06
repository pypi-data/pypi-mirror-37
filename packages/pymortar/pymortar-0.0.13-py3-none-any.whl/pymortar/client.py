import IPython
import grpc
import uuid
#import result
import pytz
import pandas as pd
import hod_pb2
import hod_pb2_grpc
import mdal_pb2
import mdal_pb2_grpc
import mortar_pb2
import mortar_pb2_grpc

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

class MortarClient:
    def __init__(self, caddr):
        self.channel = grpc.insecure_channel(caddr, options=[
                  ('grpc.max_send_message_length', 100 * 1024 * 1024),
                  ('grpc.max_receive_message_length', 100 * 1024 * 1024)
        ])
        self.stub = mortar_pb2_grpc.MortarStub(self.channel)

    def qualify(self, required):
        q = [hod_pb2.QueryRequest(query=req) for req in required]
        return self.stub.Qualify(mortar_pb2.QualifyRequest(requiredqueries=q))

    def fetch(self, request):
        aggs = {}
        for varname, aggfunclist in request["Aggregation"].items():
            aggs[varname] = mdal_pb2.Aggregation(funcs=[parse_agg_func(func) for func in aggfunclist])
        #print aggs
        vardefs = {}
        for varname, defn in request["Variables"].items():
            vardefs[varname] = mdal_pb2.Variable(
                name = varname,
                definition = defn["Definition"],
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
        
        values = [x.value for x in resp.response.values]
        if pd.np.array(values).size > 0:
            print(pd.np.array(values).shape)
            print(pd.np.array(resp.response.times).shape)
            t = resp.response.times
            v = pd.np.array(values)
            if len(resp.response.times) > pd.np.array(values).shape[1]:
                IPython.embed()
            df = pd.DataFrame.from_records(values).T
            df.index = pd.to_datetime(resp.response.times)
            return df
        return None

#class MDALClient:
#    def __init__(self, caddr):
#        self.channel = grpc.insecure_channel(caddr)
#        self.stub = mdal_pb2_grpc.MDALStub(self.channel)
#
#    def query(self, request):
#        aggs = {}
#        for varname, aggfunclist in request["Aggregation"].items():
#            aggs[varname] = mdal_pb2.Aggregation(funcs=[parse_agg_func(func) for func in aggfunclist])
#        #print aggs
#        vardefs = {}
#        for varname, defn in request["Variables"].items():
#            vardefs[varname] = mdal_pb2.Variable(
#                name = varname,
#                definition = defn["Definition"],
#                units = defn.get("Units",None),
#            )
#        #print vardefs
#        params = mdal_pb2.DataQueryRequest(
#            composition = request["Composition"],
#            aggregation = aggs,
#            variables = vardefs,
#            time = mdal_pb2.TimeParams(
#                start = request["Time"]["Start"],
#                end = request["Time"]["End"],
#                window = request["Time"]["Window"],
#                aligned = request["Time"]["Aligned"],
#            ),
#        )
#        #print params
#        tz = pytz.timezone("US/Pacific")
#        resp = self.stub.DataQuery(params, timeout=120)
#        if resp.msg != "":
#            raise Exception(resp.msg)
#        return result.Result(resp)
##        mapping = {}
##        for k, v in resp.mapping.items():
##            mapping[k] = v.uuids
##        context = {}
##        for row in resp.context:
##            context[row.uuid] = dict(row.row)
##        uuids = resp.uuids
##        data = data_capnp.StreamCollection.from_bytes_packed(resp.arrow)
##        if hasattr(data, 'times') and len(data.times):
##            times = list(data.times)
##            if len(times) == 0:
##                return pd.DataFrame(columns=uuids)
##            df = pd.DataFrame(index=pd.to_datetime(times, unit='ns', utc=False))
##            for idx, s in enumerate(data.streams):
##                df[uuids[idx]] = s.values
##            df.index = df.index.tz_localize(pytz.utc).tz_convert(tz)
##            return (df, mapping, context)
##        else:
##            df = pd.DataFrame()
##            for idx, s in enumerate(data.streams):
##                if hasattr(s, 'times'):
##                    newdf = pd.DataFrame(list(s.values), index=list(s.times), columns=[uuids[idx]])
##                    newdf.index = pd.to_datetime(newdf.index, unit='ns').tz_localize(pytz.utc).tz_convert(tz)
##                    df = df.join(newdf, how='outer')
##                else:
##                    raise Exception("Does this ever happen? Tell gabe!")
##            return (df, mapping, context)
#
#if __name__ == '__main__':
#    m = MDALClient("corbusier.cs.berkeley.edu:8088")
#
#    for windowsize in ["96h","24h","12h","6h","3h","1h","30m","15m","10m","5m","1m","30s"]:
#    #for windowsize in ["1h","30m","15m","10m","5m","1m","30s"]:
#        request = {
#            "Composition": ["temp"],
#            "Aggregation": {
#                "temp": ["MEAN"],
#            },
#            "Variables": {
#                "temp": {
#                    "Definition": """SELECT ?temp ?temp_uuid FROM ciee WHERE {
#                        ?temp rdf:type/rdfs:subClassOf* brick:Temperature_Sensor .
#                        ?temp bf:uuid ?temp_uuid
#                    };""",
#                },
#            },
#            "Time": {
#                "Start":  "2017-01-01T10:00:00-07:00",
#                "End":  "2018-05-12T10:00:00-07:00",
#                "Window": windowsize,
#                "Aligned": True,
#            },
#        }
#        resp = m.query(request)
#            
#        print len(resp.columns), len(resp)
#        print resp[resp.columns[0]].describe()

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
