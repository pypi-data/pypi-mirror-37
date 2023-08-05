import urllib
import requests

from dappy.methods import (
    GET, HEAD, POST, PUT, DELETE, CONNECT, OPTIONS, PATCH
)

from dappy.exceptions import NotSupportedException


# Users use this the define and endpoint for an API
class Endpoint:
    def __init__(self, name, path, methods=[GET], defaults={}, query_map={}):
        self.name = name
        self.path = self._prepend_slash(path)
        self.methods = methods
        self.defaults = defaults
        self.query_map = query_map

    def _prepend_slash(self, path):
        if path.startswith('/'):
            return path
        else:
            return '/' + path



# Wrapper around Endpoint that actually contains the request logic
class CompleteEndpoint:

    def __init__(self, scheme, netloc, endpoint, json=True):
        self.scheme = scheme
        self.netloc = netloc
        self.endpoint = endpoint
        self.json = json

    def __call__(self, query={}, params=None):
        return self.get(query=query, params=params)

    # Send a call to an API endpoint
    def get(self, query={}, params=None):
        self._check_method(GET)
        url = self._build_url(query, params)
        result = requests.get(url)
        return self._result_in_format(result)

    # TODO: Make these other methods make sense
    def head(self, query={}, params=None):
        self._check_method(HEAD)
        url = self._build_url(query, params)
        result = requests.head(url)
        return self._result_in_format(result)

    def post(self, data, query={}, params=None):
        self._check_method(POST)
        url = self._build_url(query, params)
        result = requests.post(url, data=data)
        return self._result_in_format(result)

    def put(self, data, query={}, params=None):
        self._check_method(PUT)
        url = self._build_url(query, params)
        result = requests.put(url, data=data)
        return self._result_in_format(result)

    def delete(self, query={}, params=None):
        self._check_method(DELETE)
        url = self._build_url(query, params)
        result = requests.delete(url)
        return self._result_in_format(result)

    def connect(self, query={}, params=None):
        self._check_method(CONNECT)
        url = self._build_url(query, params)
        result = requests.connect(url)
        return self._result_in_format(result)

    def options(self, query={}, params=None):
        self._check_method(OPTIONS)
        url = self._build_url(query, params)
        result = requests.options(url)
        return self._result_in_format(result)

    def patch(self, query={}, params=None):
        self._check_method(PATCH)
        url = self._build_url(query, params)
        result = requests.patch(url)
        return self._result_in_format(result)

    # Returns a result in the format specific by the API
    def _result_in_format(self, result):
        if self.json:
            return result.json()
        else:
            return result

    # Build the request url from what parts we have
    def _build_url(self, query={}, params=None):
        self._add_defaults(query)
        self._map_query(query)
        return urllib.parse.urlunparse((
            self.scheme,
            self.netloc,
            self.endpoint.path,
            params,
            urllib.parse.urlencode(query),
            None
        ))

    # Cycles through default params and adds them
    # if a value wasn't submitted for that param.
    # Should we do this before or after mapping the query?
    # Deciding to do this before for now because raw API param keys
    # makes more sense to me over mapped keys.
    def _add_defaults(self, query_params):
        for key in self.endpoint.defaults:
            if key not in query_params:
                query_params[key] = self.endpoint.defaults[key]

    # Allows a standard interface for APIs
    # Maps provided param keys to what the API expects
    def _map_query(self, query_params):
        for key_from, key_to in self.endpoint.query_map.items():
            if key_from in query_params:
                query_params[key_to] = query_params[key_from]
                del query_params[key_from]

    # Throws an error if method is not supported
    def _check_method(self, method):
        if method not in self.endpoint.methods:
            raise NotSupportedException((
                '{0} is not supported for this API endpoint'
            ).format(method.upper()))
