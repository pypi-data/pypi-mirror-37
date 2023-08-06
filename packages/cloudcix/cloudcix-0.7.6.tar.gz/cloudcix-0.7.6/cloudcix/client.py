# -*- coding: utf-8 -*-

"""
cloudcix.client
~~~~~~~~~~~~~~~

This module implements the CloudCIX API Client
"""

import json
import re
import requests
from collections import deque

import cloudcix.auth
import cloudcix.conf
import cloudcix.exceptions
import cloudcix.utils


class Client:
    """
    CloudCIX API Client

    The underlying class to generate the services in the :doc:`api_reference`

    There are a couple of things to note about some of the methods, namely `create`, `update`, and `partial_update`

    - The ``data`` parameter to these methods is for passing the json data to use for the creation or updating of an
      object in the database
    - The ``params`` parameter is simply for filtering lists

    .. note:: The ``kwargs`` parameter for the methods can be used to specify any other ids that are needed in the URL
    """

    def __init__(self, application, service_uri, version='v1'):
        """
        :param application: Application Name
        :param service_uri: URI of the service under the Application URL
        :param version: Optional API version, defaults to v1
        """
        self.application = application
        self.service_uri = service_uri.rstrip('/')
        self.version = version
        self.headers = {'content-type': 'application/json'}
        self.base_url = self._determine_url_for_version()

    def filter_kwargs(self, kwargs):
        """
        Filters out kwargs required by the service URL
        :param kwargs: Keyword arguments to be filtered
        :return: client_kwargs: The kwargs to be used for this client
        :return: non_client_kwargs: The unused kwargs from the parameter
        """
        pattern = re.compile(r'(?<=/\{)(?P<match>\w+)(?=\})')
        result = pattern.findall(self.service_uri)

        client_kwargs = {k: v for k, v in kwargs.items() if k in result}

        non_client_kwargs = {k: v for k, v in kwargs.items() if k not in client_kwargs}

        return client_kwargs, non_client_kwargs

    def _determine_url_for_version(self):
        """
        Determines the URL format to use for the current API version and returns it
        :returns: The URL for the correct API version for the Application
                  i.e. version 2 URL if the application supports version 2
        """
        # If it's version 2, try to connect to the version 2 URL
        if cloudcix.conf.settings.CLOUDCIX_API_VERSION == 2:
            server_url = cloudcix.conf.settings.CLOUDCIX_API_V2_URL.rstrip('/')
            protocol, url = server_url.split('://')
            url = '{}.{}'.format(self.application, url)
            blocks = ('://'.join([protocol, url]), self.service_uri)
            url = ('/'.join(blocks) + '/').lower()
            try:
                requests.get(url)
                return url
            except requests.exceptions.ConnectionError:
                # Log that we're falling back to v1
                pass
        # If it gets here, either the version is 1, or the v2 url failed
        blocks = (self.server_url, self.application, self.version, self.service_uri)
        return '/'.join(blocks) + '/'

    def prepare_url(self, pk=None, client_kwargs=None):
        """
        Prepare the absolute URL to resolve
        :param pk: The primary key value for any resource url (optional)
        :param client_kwargs: Any client kwargs to format the URL with
        :return: The prepared URL for the Client
        """
        absolute_url = self.base_url
        if pk is not None:
            absolute_url += '{}/'.format(pk)
        if client_kwargs is not None:
            try:
                return absolute_url.format(**client_kwargs)
            except KeyError as e:
                raise cloudcix.exceptions.MissingClientKwarg(e.args[0], self)
        return absolute_url

    def request(self, method, token=None, pk=None, data=None, params=None, files=None, **kwargs):
        """
        Sends a request to the API service
        :param method: The HTTP method to use
        :param token: The auth token to use
        :param pk: The primary key of the resource
        :param data: Any POST data to send
        :param params: Any GET parameters to send
        :param files: Any files to send
        :param kwargs: Any other keyword arguments
        :return: The response from the API service
        """
        client_kwargs, kwargs = self.filter_kwargs(kwargs)
        # Set headers
        if 'headers' in kwargs:
            kwargs['headers'].update(self.headers)
        else:
            kwargs['headers'] = self.headers
        # Set auth token
        if token:
            kwargs['auth'] = cloudcix.auth.TokenAuth(token)
        # Prepare request data
        kwargs['params'] = parse_parameters(params)
        kwargs['data'] = json.dumps(data, cls=cloudcix.utils.JSONEncoder)
        # Send Request
        url = self.prepare_url(pk, client_kwargs)
        response = getattr(requests, method)(url, **kwargs)

        def _dump(fn):
            # Wrapper to provide custom response.json() decoding function
            def wrapper(**kw):
                kwargs['cls'] = cloudcix.utils.JSONDecoder
                return fn(**kw)
            return wrapper

        response.json = _dump(response.json)
        return response

    def read(self, pk, token=None, params=None, **kwargs):
        """
        Reads a resource from the API service identified by the given pk (using HTTP GET with a resource id)

        :param pk: The id of the resource to read
        :param token: The User's authentication token
        :param params: Any HTTP GET parameters to be sent in the request. Used for filtering lists, etc.
        :param kwargs: Any other kwargs for the method
        :return: The read resource in the form of a :class:`requests.Response` object
        """
        return self.request(method='get', token=token, pk=pk, params=params, **kwargs)

    def list(self, token=None, params=None, **kwargs):
        """
        Retrieves a list of resources from the API service (using HTTP GET without a resource id)

        :param token: The user's authentication token
        :param params: Any HTTP GET parameters to be sent in the request. Used for filtering lists, etc.
        :param kwargs: Any other kwargs for the method
        :return: A list of resources in the form of a :class:`requests.Response` object
        """
        return self.request(method='get', token=token, params=params, **kwargs)

    def get_all(self, token=None, params=None, **kwargs):
        """
        Retrieves the entire list of items given the params

        :param token: The user's authentication token
        :param params: Any HTTP GET parameters to be sent in the request. Used for filtering lists, etc.
        :param kwargs: Any other kwargs for the method
        :return: A list of all the resources found given the parameters supplied
        """
        params = params or {}
        params['page'] = 0
        params['limit'] = 100
        items = deque()
        response = self.list(token, params, **kwargs).json()
        total_records = response['_metadata'].get(
            'total_records',
            response['_metadata']['totalRecords'],
        )
        items.extend(response['content'])
        while len(items) < total_records:
            params['page'] += 1
            content = self.list(token, params, **kwargs).json()['content']
            items.extend(content)
        return list(items)

    def create(self, token=None, data=None, params=None, **kwargs):
        """
        Creates a new resource using the API service (using HTTP POST)

        :param token: The user's authentication token
        :param data: Any POST data to send in the request
        :param params: Any HTTP GET parameters to be sent in the request. Used for filtering lists, etc.
        :param kwargs: Any other kwargs for the method
        :return: The response from the API in the form of a :class:`requests.Response` object
        """
        return self.request(method='post', token=token, data=data, params=params, **kwargs)

    def update(self, pk, token=None, data=None, params=None, **kwargs):
        """
        Updates a resource identified by the given pk with the sent data (using HTTP PUT)

        :param pk: The id of the resource to update
        :param token: The user's authentication token
        :param data: The data to be sent in the PUT request
        :param params: Any HTTP GET parameters to be sent in the request. Used for filtering lists, etc.
        :param kwargs: Any other kwargs for the method
        :return: The response from the API in the form of a :class:`requests.Response` object
        """
        return self.request(method='put', token=token, pk=pk, data=data, params=params, **kwargs)

    def partial_update(self, pk, token=None, data=None, params=None, **kwargs):
        """
        Updates a resource identified by the given pk with the sent data (using HTTP PATCH).
        The difference between this and `update` is that this method does not require an entire object be sent.

        :param pk: The id of the resource to update
        :param token: The user's authentication token
        :param data: The data to be sent in the PUT request
        :param params: Any HTTP GET parameters to be sent in the request. Used for filtering lists, etc.
        :param kwargs: Any other kwargs for the method
        :return: The response from the API in the form of a :class:`requests.Response` object
        """
        return self.request(method='patch', token=token, pk=pk, data=data, params=params, **kwargs)

    def delete(self, pk, token=None, params=None, **kwargs):
        """
        Deletes a resource identified by the given pk (using HTTP DELETE)

        :param pk: The id of the resource to delete
        :param token: The user's authentication token
        :param params: Any HTTP GET parameters to be sent in the request. Used for filtering lists, etc.
        :param kwargs: Any other kwargs for the method
        :return: The response from the API in the form of a :class:`requests.Response` object
        """
        return self.request(method='delete', token=token, pk=pk, params=params, **kwargs)

    def __repr__(self):
        """
        Creates a string representation of this Client instance.
        """
        return '<Client [{}]>'.format(self.base_url)

    @property
    def server_url(self):
        """
        :return: The API Service URL
        """
        return cloudcix.conf.settings.CLOUDCIX_API_URL.rstrip('/')


def parse_parameters(params):
    """
    Prepares parameters into an acceptable format for the API Service
    :param params: The parameters to prepare
    :return: The prepared version of the parameters
    """
    if not params:
        return {}
    for k, v in params.items():
        if hasattr(v, 'isoformat'):
            params[k] = v.isoformat()
        elif isinstance(v, bool):
            params[k] = str(v).lower()
        elif hasattr(v, '__iter__'):
            params[k] = str(v).replace(' ', '')
    return params
