from dorcas_sdk_python import Sdk


def authorize_via_email_only(sdk, email_address, return_token=True):
    """ Sends an authorization request for the user, using the email alone. """
    if not isinstance(sdk, Sdk):
        raise TypeError('sdk needs to be an instance of Sdk')
    if not isinstance(email_address, str):
        raise TypeError('email needs to be a string value')
    authorize = sdk('service', 'Authorization')
    authorize.add_body_param('email', email_address)
    response = authorize.send(method='post', path='email')
    if not response.is_successful() or not return_token:
        return response
    return response.access_token


def login_via_password(sdk, username, password, return_token=True):
    """ Performs a login using a username(email) + password combination. """
    if not isinstance(sdk, Sdk):
        raise TypeError('sdk needs to be an instance of Sdk')
    if not isinstance(username, str) or not isinstance(password, str):
        raise TypeError('username, and password needs to be a string values')
    password_login = sdk('service', 'PasswordLogin')
    password_login.add_body_param('username', username)
    password_login.add_body_param('password', password)
    response = password_login.send(method='post')
    if not response.is_successful() or not return_token:
        return response
    return response.access_token


def create_account(sdk, **kwargs):
    """ Makes a call to the registration service to create a new user account. """
    if not isinstance(sdk, Sdk):
        raise TypeError('sdk needs to be an instance of Sdk')
    registration = sdk('service', 'Registration')
    for k, v in kwargs.items():
        registration.add_body_param(k, v)
    return registration.send(method='post')
