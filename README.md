python-browserstack
===================

This is a python library for the BrowserStack API. Usage examples are below-

For installing the library, you can use easy_install or pip -

`easy_install Python-BrowserStack`

For using the library and it functions, you have to import the library and make a client object by passing your
BrowserStack username and password - 

```
from browserstack import browserstack
client = browserstack.BrowserStack(username = 'sidchilling@gmail.com', password = 'your_password')
```

Then you call functions using the client objects.

```
client.get_browsers()
```
Gets all the browsers, devices and versions

```
client.get_browsers(os = 'mac')
```
Gets all the browsers only for the OS passed
```
client.create_worker(url = 'http://siddharthsaha.weebly.com', **kwargs)
```
Creates a worker for the URL using the
settings that you have passed. The settings can be `(os, browser, version)` or `(os, device, version)`. Have a look
at the end of the library file to see the test cases
```
client.delete_worker(id)
```
Deletes the worker whose ID is passed
```
client.get_workers()
```
Gets all the workers
```
client.get_api_status
```
Gets your API status

All the functions returns JSON output.
