easywsy Documentation
=====================

**easywsy** is a high-level API based on suds for developing connections to any Web Service. The main feature is the readability and simpleness of the code required to connect to a Web Service.

For example, this code connects to a Web Service, and use one of its functions to sum two numbers:

```python
from easywsy import WebService

class WSCalc(WebService):
ws = WSCalc(WSURL)
request_data = {
    'Add': {
        'intA': 10,
        'intB': 20,
    }
}
ws.add(request_data)
response = ws.request('Add')
# response will then be 30
```

Another big feature is the support for dynamic checks on the fields sent to the Web Service. This allows the developer to check the values that will be send to the Web before sending them, preventing a connection to the internet that will always return an error.

This is achieved through method decoration as follows:

```python
from easywsy import wsapi

@wsapi.check(['intA', 'intB'])
def validation_method(value):
    if isinstance(value, int):
        return True
    else:
        return False
```

Following the previous example, this method will be called twice, each time with the value of intA and intB in the `value` paramenter. If the method returns False, a predefined error will be raised, and if it returns True, the flow continues.
