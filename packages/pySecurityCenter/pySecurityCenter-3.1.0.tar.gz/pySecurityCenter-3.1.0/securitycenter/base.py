from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
import logging


class APIError(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return repr('[%s]: %s' % (self.code, self.msg))


class BaseAPI(object):
    _pre = ''
    _host = None
    _port = 443
    _token = None
    _ssl_verify = False
    verbose = False
    _log = None
    _session = None
    _timeout = (30, 300)

    def __init__(self, host, port=443, ssl_verify=False, scheme='https', log=False, timeout=None):
        '''BaseAPI Initialization'''
        self._session = requests.Session()
        self._host = host
        self._port = port
        self._ssl_verify = ssl_verify
        self._scheme = scheme
        if log:
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            self._log = logging.getLogger(__name__)
            self._log.setLevel(logging.DEBUG)
            self._log.addHandler(ch)
            self._log.propagate = True
            requests_log = logging.getLogger("requests.packages.urllib3")
            requests_log.setLevel(logging.DEBUG)
            requests_log.addHandler(ch)
            requests_log.propagate = True
        if timeout:
            self._timeout = timeout

    def _reset_session(self):
        self._session = requests.Session()

    def _url(self, path):
        return '%s://%s:%s/%s%s' % (self._scheme, self._host, self._port, self._pre, path)

    def _builder(self, **kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        kwargs['verify'] = self._ssl_verify
        if not self._ssl_verify:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        if self._log:
            self._log.debug('REQUEST: %s' % kwargs)
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self._timeout
        return kwargs

    def _resp_error_check(self, response):
        try:
            d = response.json()
            if 'error' in d and d['error']:
                raise APIError(response.status_code, d['error'])
        except ValueError:
            pass
        return response

    def head(self, path, **kwargs):
        '''Calls the specified path with the HEAD method'''
        resp = self._session.head(self._url(path), **self._builder(**kwargs))
        if 'stream' in kwargs:
            return resp
        else:
            return self._resp_error_check(resp)

    def get(self, path, **kwargs):
        '''Calls the specified path with the GET method'''
        resp = self._session.get(self._url(path), **self._builder(**kwargs))
        if 'stream' in kwargs:
            return resp
        else:
            return self._resp_error_check(resp)

    def post(self, path, **kwargs):
        '''Calls the specified path with the POST method'''
        resp = self._session.post(self._url(path), **self._builder(**kwargs))
        if 'stream' in kwargs:
            return resp
        else:
            return self._resp_error_check(resp)

    def put(self, path, **kwargs):
        '''Calls the specified path with the PUT method'''
        resp = self._session.put(self._url(path), **self._builder(**kwargs))
        if 'stream' in kwargs:
            return resp
        else:
            return self._resp_error_check(resp)

    def patch(self, path, **kwargs):
        '''Calls the specified path with the PATCH method'''
        resp = self._session.patch(self._url(path), **self._builder(**kwargs))
        if 'stream' in kwargs:
            return resp
        else:
            return self._resp_error_check(resp)

    def delete(self, path, **kwargs):
        '''Calls the specified path with the DELETE method'''
        resp = self._session.delete(self._url(path), **self._builder(**kwargs))
        if 'stream' in kwargs:
            return resp
        else:
            return self._resp_error_check(resp)
