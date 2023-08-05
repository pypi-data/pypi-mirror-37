# SG Markets XSF API - ROLLBOX - Futures RollBox v1


## 1- Introduction

This repo is meant to make it easy for clients (and employees) to tap SG XSF APIs.  

This repo contains:
+ a ready-to-use [demo notebook](https://nbviewer.jupyter.org/urls/gitlab.com/sgmarkets/sgmarkets-api-xsf-rollbox/raw/master/demo_sgmarkets_api_xsf_rollbox.ipynb)
+ the underlying library in folder [sgmarkets_api_xsf_rollbox](https://gitlab.com/sgmarkets/sgmarkets-api-xsf-rollbox/tree/master/sgmarkets_api_xsf_rollbox)


## 2 - Install

From terminal:
```bash
# download and install package from pypi.org
pip install sgmarkets_api_xsf_rollbox

# launch notebook
jupyter notebook
```
Create a notebook or run the demo notebook and modify it to your own use case.


## 3 - User guide

Read the [demo notebook](https://nbviewer.jupyter.org/urls/gitlab.com/sgmarkets/sgmarkets-api-xsf-rollbox/raw/master/demo_sgmarkets_api_xsf_rollbox.ipynb).

The key steps are the following.

### 3.1 - Read the info

The package contains the corresponding API swagger url and contact info:

```python
import sgmarkets_api_xsf_rollbox as ROLLBOX
# info about ROLLBOX
ROLLBOX.info()
```

### 3.2 - Define you credentials

See the user guide in the [sgmarkets-api-auth repo](https://gitlab.com/sgmarkets/sgmarkets-api-auth#3-user-guide)


### 3.3 - Pick an endpoint

Select it from the list of those available in the package.  

```python
import sgmarkets_api_xsf_rollbox as ROLLBOX
# Examples
ep = ROLLBOX.endpoint.v1_underlyings
ep = ROLLBOX.endpoint.v1_relative_roll
```

### 3.4 - Create the associated request

Each end point comes with a `Request` object.  

```python
# For all endpoints
rq = ep.request()
```

And fill the object with the necessary data.  
This part is specific to the endpoint selected.  
See the [demo notebook](https://nbviewer.jupyter.org/urls/gitlab.com/sgmarkets/sgmarkets-api-xsf-rollbox/raw/master/demo_sgmarkets_api_xsf_rollbox.ipynb) for examples.  

Then explore your `Request` object to make sure it is properly set.
```python
# For all endpoints
# display the structure of the object
rq.info()
```

### 3.5 - Call the API

You can call the API directly from the `Request` object.  

```python
# For all endpoints
# a is an Api object (see 3.2)
res = rq.call_api(a)
```

The returned object is a `Response` object associated to this endpoint.  
You can explore it starting with

```python
# For all endpoints
# display the structure of the object
res.info()
```

### 3.6 - Save and show the results

As `.csv` file.

```python
# For all endpoints
# save to disk
res.save()
```

The `Response` objects are different for each endpoint.  
See the [demo notebook](https://nbviewer.jupyter.org/urls/gitlab.com/sgmarkets/sgmarkets-api-xsf-rollbox/raw/master/demo_sgmarkets_api_xsf_rollbox.ipynb) for examples.  


### 3.7 - Build a Dashboard

As `.html` file.  
The resulting html file can be viewed independently from the Jupyter notebook context.

```python
# endpoint ROLLBOX.endpoint.v1_analysis
res.build_dashboard()
```

See the [demo notebook](https://nbviewer.jupyter.org/urls/gitlab.com/sgmarkets/sgmarkets-api-xsf-rollbox/raw/master/demo_sgmarkets_api_xsf_rollbox.ipynb) for an example.  
