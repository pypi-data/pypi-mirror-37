import logging
import requests
from requests import HTTPError

name = "dorcas_sdk_python"
__version__ = '0.0.1'

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())


def get_dorcas_base_url(environment='staging'):
    """ Returns the base URL to use for all requests against the API. """
    environments = dict(local='http://api.dorcas.local', staging='https://staging-api.dorcas.ng',
                        production='https://api.dorcas.ng')
    if not isinstance(environment, str) or environment not in environments.keys():
        environment = 'staging'
    return environments[environment]


def remove_slashes_from_url_path(path):
    """ It strips the start, and ending slashes from a URL path. """
    if not isinstance(path, str):
        raise TypeError('The path needs to be a string')
    if path.startswith('/'):
        path = path[1:]
    if path.endswith('/'):
        path = path[0:-1]
    return path


class Sdk:
    def __init__(self, client_id='', client_secret='', auth_token=None, environment='staging'):
        """ Instantiates the SDK.

        It provides some useful helpers to assist in setting
        """
        if not isinstance(client_id, str) or not isinstance(client_secret, str):
            raise TypeError('The client_id, and client_secret should be string values')

        if auth_token is not None and not isinstance(auth_token, str):
            auth_token = None

        if environment is None or environment not in ['production', 'staging', 'local']:
            environment = 'staging'

        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_token = auth_token
        self.environment = environment

    def __call__(self, model_type, model_name, **kwargs):
        """ Provides a quick way to instantiate resources, and services in the SDK.

        For example:
        sdk = Sdk()
        sdk('resource', 'User', option1='abc', option2='def', option3='ghi')
        """
        if not isinstance(model_type, str) or not isinstance(model_name, str):
            raise TypeError('The type, and type_name need to be strings')
        model_type = model_type.lower()
        if model_type not in ['resource', 'service']:
            raise ValueError('An invalid type was provided. Valid types are: resource, service')
        if model_type == 'resource':
            from . import resources
            cls = getattr(resources, model_name)
            return cls(self, **kwargs)
        else:
            from . import services
            cls = getattr(services, model_name)
            return cls(self, **kwargs)


class PayloadItem:
    """
    A simple payload object.
    """
    def __init__(self, param_name, param_value, **kwargs):
        """Initialise the payload item with a name, value, and any extra keys.
        :param param_name:
        :param param_value:
        :param kwargs:
        """
        self.name = param_name
        self.value = param_value
        self.extras = kwargs

    def get_item(self):
        """Returns the payload parameter as a simple dictionary object."""
        params = dict(name=self.name, value=self.value)
        for k, v in self.extras.items():
            params[k] = v
        return params

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        components = ', '.join([key + '=' + str(value) for key, value in self.extras])
        return 'PayloadItem<name=' + self.name + ', value=' + str(self.value) + components + '>'


class PayloadBag:
    """ Provides a simple container for payload items. """

    def __init__(self):
        """Initialises the payload container object."""
        self.bag = []

    def is_empty(self):
        """ Checks if the parameter bag is currently empty. """
        return len(self.bag) == 0

    def add_simple(self, param_name, param_value):
        """ Adds a new payload item directly to the bag. """
        if not isinstance(param_name, str):
            raise TypeError('The param_name should be a string')
        self.bag.append(PayloadItem(param_name, param_value))
        return self

    def add_item(self, item):
        if not isinstance(item, PayloadItem):
            raise TypeError('item must be an instance of PayloadItem')
        self.bag.append(item)
        return self

    def clear_items(self):
        self.bag.clear()
        return self

    def remove_item(self, index):
        self.bag.pop(index)
        return self

    def remove_item_by_name(self, param_name):
        if self.has_item(param_name):
            self.bag = [bag for bag in self.bag if bag.name != param_name]
        return self

    def set_item_by_name(self, param_name, param_value):
        """ Replaces the value for a key with the new value."""
        self.remove_item_by_name(param_name)
        self.add_simple(param_name, param_value)

    def set_items(self, payload, clear_items=True):
        """ Sets a large number of values at once in the payload; optionally clearing the previous items."""
        if not isinstance(payload, dict):
            raise TypeError('payload needs to be an instance of dict')
        if clear_items:
            self.clear_items()
        for k, v in payload.items():
            self.add_simple(k, v)
        return self

    def has_item(self, key):
        """ Checks if the key is contained in the payload. """
        return key in self.to_payload()

    def get_item(self, index):
        """ Returns the item at that index."""
        if index < 0:
            raise OverflowError('The item index should be: 0 <= index < {0}'.format(len(self.bag)))
        if index >= len(self.bag):
            raise OverflowError('The provided index value is greater than the size of the bag')
        return self.bag[index]

    def get_item_by_name(self, param_name):
        """ Gets the item with a param key by the provided name. """
        filtered = [bag for bag in self.bag if bag.name == param_name]
        if len(filtered) > 0:
            return filtered[0]
        return None

    def to_payload(self, as_multipart=False):
        if not as_multipart:
            return {item.name: item.value for item in self.bag}
        return {item.name: (item.extras['filename'], item.value) for item in self.bag if 'filename' in item.extras}

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        items = [str(item) for item in self.bag]
        return str(items)


class DorcasException(Exception):
    """ The exception thrown when something goes wrong. """
    def __init__(self, message, context=None):
        self.message = message
        if isinstance(context, dict):
            self.context = context
        else:
            self.context = {}


class DorcasRequest:
    """ Base class for use in communicating with the Dorcas API. """
    def __init__(self, environment='staging', query=None, payload=None, multipart_payload=None, headers=None):
        """ Instantiates the Request instance.

        :param query:
        :param payload:
        :param multipart_payload:
        :param headers:
        """
        if not isinstance(environment, str):
            environment = 'staging'

        if query is None or not isinstance(query, PayloadBag):
            query = PayloadBag()

        if payload is None or not isinstance(payload, PayloadBag):
            payload = PayloadBag()

        if multipart_payload is None or not isinstance(multipart_payload, PayloadBag):
            multipart_payload = PayloadBag()

        if headers is None or not isinstance(headers, PayloadBag):
            headers = PayloadBag()

        self.environment = environment
        self.body = payload
        self.multipart = multipart_payload
        self.query_parameters = query
        self.headers = headers

    def get_path(self):
        """ Get the path for this request. """
        return ''

    def prefill_header(self):
        """ Adds some items that need to be passed along in the header. """
        self.headers.add_simple('User-Agent', 'dorcas-sdk-python/' + __version__)
        if self.requires_authorization():
            self.headers.add_simple('Authorization', self.get_authorization_header())

    def prefill_body(self):
        return True

    def get_authorization_header(self):
        """ Returns the 'Authorization' header value for the request. """
        return ''

    def requires_authorization(self):
        """ Whether or not the current model requires a 'Authorization' header. """
        return False

    def requires_payload_validation(self):
        return False

    def add_body_param(self, param_name, param_value, overwrite=True):
        """ Adds a new parameter to the request body for DELETE, POST, and PUT requests. """
        if self.body.has_item(param_name) and not overwrite:
            return self
        self.body.set_item_by_name(param_name, param_value)

    def add_query_param(self, param_name, param_value, overwrite=True):
        """ Adds a new parameter to the query part of a request. """
        if self.query_parameters.has_item(param_name) and not overwrite:
            return self
        self.query_parameters.set_item_by_name(param_name, param_value)

    def add_multipart_param(self, param_name, filename, overwrite=True):
        """ Adds a new parameter to the request body of a multipart/form-data request for POST requests. """
        if self.multipart.has_item(param_name) and not overwrite:
            return self
        self.multipart.add_item(PayloadItem(param_name, open(filename, 'rb'), filename=filename))

    def validate_payload(self):
        """ Called to validate the request payload of a request. """
        raise DorcasException('Override this method for resources/services that need validation')

    def send(self, method='get', path=''):
        """ Sends a HTTP request to the API. """
        if self.requires_authorization() and self.get_authorization_header() in ['', 'Bearer ']:
            raise DorcasException('Calls to this endpoint require authentication. Set the auth_token for the SDK.')
        self.prefill_header()
        self.prefill_body()
        # pre-fills the header, and body with some defaults from the resource/service
        method = method.lower()
        try:
            if self.requires_payload_validation():
                # for non-GET requests, we try to run the data/payload validation
                self.validate_payload()

            url = '/'.join([get_dorcas_base_url(self.environment), remove_slashes_from_url_path(self.get_path()),
                            remove_slashes_from_url_path(path)])
            # set the base URL for the request
            if url.endswith('/'):
                # strip off the ending slash
                url = url[0:-1]
            params = None
            body_payload = None
            multipart_payload = None
            headers = None

            if not self.headers.is_empty():
                headers = self.headers.to_payload()

            if not self.query_parameters.is_empty():
                params = self.query_parameters.to_payload()

            if not self.body.is_empty():
                body_payload = self.body.to_payload()

            if not self.multipart.is_empty():
                multipart_payload = self.multipart.to_payload(as_multipart=True)

            if multipart_payload is not None and len(multipart_payload) > 0:
                for k, v in body_payload:
                    multipart_payload[k] = v
                body_payload = None
            if method == 'get':
                response = requests.get(url, params=params, headers=headers)
            elif method == 'delete':
                response = requests.delete(url, params=params, json=body_payload, headers=headers)
            elif method == 'put':
                response = requests.put(url, params=params, json=body_payload, headers=headers)
            else:
                if multipart_payload is None or len(multipart_payload) == 0:
                    response = requests.post(url, params=params, json=body_payload, headers=headers)
                else:
                    # this part has not been tested -- so it can't be considered as supported yet
                    response = requests.post(url, params=params, files=multipart_payload, headers=headers)

            return DorcasResponse(response.json(), response.status_code, response=response)
        except HTTPError as e:
            return DorcasResponse(e.response.json(), e.response.status_code, response=e.response)
        except ConnectionError:
            return DorcasResponse(dict(message='Server connection failed', errors=dict(title='Connection failed')), 0)
        except TimeoutError:
            return DorcasResponse(dict(message='Request timed out', errors=dict(title='Request timeout')), 0)


class DorcasResponse:
    """ This class encapsulates a standard Dorcas response.

    It allows access to the various keys in the JSON response, as well as (optional) response object from which the
    instance was created - when provided (it defaults to None).

    Additional information can be gotten from the response object when available, like so:

    self.response.headers['content-type']   # application/json
    self.response.cookies['cookie_name']    # cookie value

    see: http://docs.python-requests.org/en/master/user/quickstart/#response-headers
    """
    def __init__(self, json, http_status=200, response=None):
        if not isinstance(json, dict):
            raise TypeError('The json response should be a dict instance')
        if not isinstance(http_status, int):
            raise TypeError('The http_status need to be an integer value; usually between 100 - 504')
        self.json = json
        self.http_status = http_status
        # this was added to grant access to the actual response object for use with accessing
        # other response data. e.g. cookies, headers
        # see: http://docs.python-requests.org/en/master/user/quickstart/#response-headers
        # self.response.headers['content-type']
        self.response = response

    def __getattr__(self, key):
        """ Returns a value with the specified key from the JSON (dict) response. """
        return self.json.get(key, None)

    def is_successful(self):
        return 200 <= self.http_status < 300

    def code(self):
        return self.__getattr__('code')

    def message(self):
        return self.__getattr__('message')

    def data(self):
        return self.__getattr__('data')

    def errors(self):
        return self.__getattr__('errors')

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'DorcasResponse<JSON=' + str(self.json) + ', http_status=' + str(self.http_status) + '>'

