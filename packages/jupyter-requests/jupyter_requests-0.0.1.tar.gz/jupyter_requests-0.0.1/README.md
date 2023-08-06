# Jupyter Requests

Send requests to a Jupyter server. Useful for testing/exploring the Jupyter RESTful API.

**Command Line**

Make a request to a jupyter server from the command line.
```
jupyter_requests get api/contents
```

**API**

```python
from jupyter_requests import JupyterRequester
import pprint 

# Port number of the server
port = 8888

# Get a requester object.
r = JupyterRequester(port=port)

endpoint = 'api/contents'
response = r.get(endpoint)

pprint(response)
```