YARNBackend
===========

A proof of concept extension of joblib which allows a sklearn script to
use the compute available in a YARN cluster.

The YARNBackend uses a YARNPool to spawn workers inside YARN container
which then execute the jobs.


Running
=======

A minimal change is required to your existing scikit learn script:


```python
from sklearn.externals.joblib.parallel miport register_parallel_backend
from yarnbackend import YarnBackend
register_parallel_backend("default", YarnBackend)
```


This will overwrite the current backend with the YarnBackend. However,
to be able to register a parallel backend, you will need to
* Run a development branch of scikit
* Replace the externals/joblib with this branch 
https://github.com/NielsZeilemaker/joblib/tree/custom_backend

Have fun, and good luck....
