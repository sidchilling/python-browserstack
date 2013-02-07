import requests
from datetime import datetime
try:
    import json
except ImportError:
    import simplejson as json

class BrowserStack(object):

    ENDPOINT = 'http://api.browserstack.com/2'
    VERSION = '2'

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

    def get_browsers(self, os = None):
	'''Function to get all the browsers and other data. If you want for a particular OS
	then you can pass a OS name
	'''
	browser_data = self._make_request(url = 'browsers', type = 'GET', data = {})
	if os:
	    return browser_data.get(os) if os in browser_data else []
	else:
	    return browser_data

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
	return self._make_request(url = 'worker/%s' %(id), type = 'DELETE', data = {})

    def get_workers(self):
	'''Returns all the workers'''
	return self._make_request(url = 'workers', type = 'GET', data = {})

    def get_api_status(self):
	'''Returns the API status'''
	return self._make_request(url = 'status', type = 'GET', data = {})

# Test Cases -- 
if __name__ == '__main__':
    browserstack = BrowserStack(username = 'sidchilling@gmail.com', 
	    password = 'yourpassword')
    print browserstack.get_browsers()
    kwargs = {
	    'os' : 'win',
	    'browser' : 'ie',
	    'version' : '7.0'
	    }
    print browserstack.create_worker(url = 'http://siddharthsaha.weebly.com', **kwargs)
    kwargs = {
	    'os' : 'ios',
	    'device' : 'iPad',
	    'version' : '3.2'
	     }
    ios_worker = browserstack.create_worker(url = 'http://siddharthsaha.weebly.com', **kwargs)
    print ios_worker
    print browserstack.delete_worker(id = ios_worker.get('id'))
    print browserstack.get_api_status()
    workers = browserstack.get_workers()
    print workers
    # Delete all workers
    for worker in workers:
	browserstack.delete_worker(id = worker.get('id'))
    print browserstack.get_workers()
