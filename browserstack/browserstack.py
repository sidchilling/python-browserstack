import requests
from datetime import datetime
try:
    import json
except ImportError:
    import simplejson as json

class BrowserStack(object):

    ENDPOINT = 'http://api.browserstack.com/3'
    VERSION = '3'

    def __init__(self, username, password):
	assert username and password, 'username and password are required'
	self.username = username
	self.password = password
    
    def _make_request(self, url, type, data = {}):
	url = '%s/%s' %(self.ENDPOINT, url)
	if type == 'HEAD':
	    r = requests.head(url = url, params = data,
		    auth = (self.username, self.password))
	elif type == 'GET':
	    r = requests.get(url = url, params = data,
		    auth = (self.username, self.password))
	elif type == 'POST':
	    r = requests.post(url = url, params = data,
		    auth = (self.username, self.password))
	elif type == 'DELETE':
	    r = requests.delete(url = url, params = data,
		    auth = (self.username, self.password))
	if r.status_code == 200:
	    return json.loads(r.content)
	elif r.status_code in [422, 403]:
	    raise Exception('Validation Error. %s' %(json.loads(r.content)))
	elif r.status_code == 401:
	    raise Exception('Unauthorized User')

    def get_browsers(self, flat = False):
	'''Function to get all the browsers and other data. If you want for a particular OS
	then you can pass a OS name
	'''
	url = 'browsers' if not flat else 'browsers?flat=true'
	return self._make_request(url = url, type = 'GET')

    def create_worker(self, url, **kwargs):
	'''Creates a new worker. kwargs can be (os, browser, version) 
	or (os, device, version)
	'''
	data = {
		'url' : url
	       }
	for key in kwargs:
	    data[key] = kwargs[key]
	return self._make_request(url = 'worker', type = 'POST', data = data)

    def delete_worker(self, id):
	'''Delete a particulat worker'''
	return self._make_request(url = 'worker/%s' %(id), type = 'DELETE')
    
    def get_worker_status(self, id):
	'''Get the status of a worker'''
	return self._make_request(url = 'worker/%s' %(id), type = 'GET')

    def get_workers(self):
	'''Returns all the workers'''
	return self._make_request(url = 'workers', type = 'GET')

    def get_api_status(self):
	'''Returns the API status'''
	return self._make_request(url = 'status', type = 'GET')

# Test Cases -- 
if __name__ == '__main__':
    browserstack = BrowserStack(username = 'sidchilling@gmail.com', 
	    password = 'nitrkl123')
    print browserstack.get_browsers()
    print browserstack.get_browsers(flat = True)
