# Backend

## v2

### General Information

Ver. 2.0 uses the `Sanic`, replacing `Flask` as the server framework due to the fast nature and asynchronicity for handling requests. Also replaces `unittest` with `pytest` as module for testing due to support of asynchronous handles for testing endpoints.

### How to Use

First of all, ensure that all of the required packages are installed. They are listed as follows:
```
    pip install Sanic 
    pip install setuptools 
    pip install requests    
    pip install flask-cors
    pip install numpy
    pip install scipy
    pip install pandas
```

With them installed, you can proceed to the next step.

To run the server directly through terminal, use this command in the terminal:
```
    sanic cieapi.api --workers=4
```

To run tests and see coverage, download the following packages, then run the given commands:

```
    pip install pytest
    pip install coverage
```

```
    coverage run -m pytest cieapi_test.py
    coverage report -i -m
```

### Credit

This part of the repository contains code from another repository, as well as code based from an answer on StackOverflow.

As this project is based as an extension of an already existing application, code from the following repository has been reused here to both reuse it for sustainability, as well as to keep consistency between the apps. This repository is located at: https://github.com/ifarup/ciefunctions/tree/master.

Specifically, in this folder, there are three specific files included from the repository, used within this project:
    - `/compute.py`, from https://github.com/ifarup/ciefunctions/blob/master/tc1_97/compute.py
    - `/utils.py`, from https://github.com/ifarup/ciefunctions/blob/master/tc1_97/utils.py
    - `/styles/description.py`, from https://github.com/ifarup/ciefunctions/blob/master/tc1_97/description.py

The usage of these files within the project are covered within the other code of the repository. For all instances of reusage, there has been made a solid attempt to list both line and module the code was derived/used from.

In addition to this, code from a StackOverflow post has been included within the project, within the `/graph.py` module. The code was for transposing within JavaScript, a process necessary for the diagram endpoint. The website of which the code was derived is located here: https://stackoverflow.com/a/36164530.

## v1

The `/v1/` endpoints are not supported on this service. 