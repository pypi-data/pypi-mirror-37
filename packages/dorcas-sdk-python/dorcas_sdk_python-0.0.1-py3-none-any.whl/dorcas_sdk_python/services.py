from . import DorcasException, DorcasRequest, Sdk


class Service(DorcasRequest):
    """ The base service class inherited by other resources. """
    def __init__(self, sdk, **kwargs):
        """ Base class for services. """
        if not isinstance(sdk, Sdk):
            raise TypeError('sdk must be an instance of Sdk')
        self.sdk = sdk
        self.options = kwargs
        super().__init__(sdk.environment)

    def get_authorization_header(self):
        """ Returns the 'Authorization' header value to place in requests. """
        if len(self.sdk.auth_token) == 0:
            return ''
        return 'Bearer ' + self.sdk.auth_token

    def requires_authorization(self):
        """ For the most part, service requests do not require authentication. """
        return False


class Authorization(Service):
    """ Helps interact with the direct authorization endpoint. """
    def get_path(self):
        return 'auth'


class PasswordLogin(Service):
    """ Helps interact with the password login endpoint. """
    def prefill_body(self):
        """ Adds some accompanying data that normally won't be provided by the user. """
        self.body.set_item_by_name('client_id', self.sdk.client_id)
        self.body.set_item_by_name('client_secret', self.sdk.client_secret)
        self.body.set_item_by_name('grant_type', 'password')
        self.body.set_item_by_name('scope', '')

    def get_path(self):
        return 'oauth/token'


class Company(Service):
    """ Helps access data regarding the currently authenticated company. """
    def requires_authorization(self):
        """ Calls to the service endpoint require authentication. """
        return True

    def get_path(self):
        return 'company'


class Metrics(Service):
    """ Provides some metrics for the currently logged in account. """
    def requires_authorization(self):
        """ Calls to the service endpoint require authentication. """
        return True

    def requires_payload_validation(self):
        """ Calls to this endpoint require some payload validation."""
        return True

    def validate_payload(self):
        """ Validates that the REQUIRED 'metrics' key is provided in the request."""
        if self.query_parameters.has_item('metrics'):
            return True
        raise DorcasException('You need to supply the metrics key in the request.')

    def get_path(self):
        return 'statistics'


class Profile(Service):
    """ Provides access to the currently authenticated user's profile information. """
    def requires_authorization(self):
        """ Calls to the service endpoint require authentication. """
        return True

    def get_path(self):
        return 'me'


class Registration(Service):
    """ Provides access to the profile registration service. """
    def prefill_body(self):
        """ Adds some accompanying data that normally won't be provided by the user. """
        self.body.set_item_by_name('client_id', self.sdk.client_id)
        self.body.set_item_by_name('client_secret', self.sdk.client_secret)

    def validate_payload(self):
        """ Validates that the REQUIRED 'param' keys are provided in the request.

        Some are automatically added to the request by the service: client_id, client_secret - and thus, do not need
        to be supplied by the caller.
        """
        required_keys = ["client_id", "client_secret", "email", "password", "firstname", "lastname", "phone", "company"]
        payload = self.body.to_payload()
        missing_keys = [key for key in required_keys if key not in payload]  # get the keys not present
        if len(missing_keys) == 0:
            return True
        raise DorcasException('Some required parameters are missing in the request.', dict(missing_params=missing_keys))

    def get_path(self):
        return 'register'


class Store(Service):
    """ Grants unauthenticated access to the store service."""
    def get_path(self):
        return 'store'
