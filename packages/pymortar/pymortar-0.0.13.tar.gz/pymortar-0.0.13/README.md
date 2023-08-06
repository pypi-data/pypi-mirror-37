# PyMortar

```
python3 setup.py sdist bdist_wheel
twine upload dist/*
```

Run plasma
```
pip install pyarrow
plasma_store -m 1000000 -s /tmp/plasma
```
