from . import DorcasException, DorcasRequest, Sdk


class Resource(DorcasRequest):
    """ The base resource class inherited by other resources. """
    def __init__(self, sdk, **kwargs):
        """ Base class for resources. """
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
        """ For the most part, requests for resources require authentication. """
        return True


class Advert(Resource):
    """ Resource for interacting with adverts. """
    def get_path(self):
        return 'adverts'


class Application(Resource):
    """ Resource for interacting with developer application records. """
    def get_path(self):
        return 'developers/applications'


class AppStore(Resource):
    """ Resource for interacting with apps on the app store. """
    def requires_payload_validation(self):
        """ Requests need to be validated to contain something. """
        return True

    def validate_payload(self):
        if self.query_parameters.has_item('oauth_client'):
            return True
        raise DorcasException('You need to supply the oauth_client details in the request')

    def get_path(self):
        return 'developers/app-store'


class Blog(Resource):
    """ Resource for interacting with blog resources/sub-resources. """
    def get_path(self):
        return 'blog'


class Company(Resource):
    """ Resource for interacting with companies. """
    def get_path(self):
        return 'companies'


class ContactField(Resource):
    """ Resource for interacting with contact-field records. """
    def get_path(self):
        return 'contact-fields'


class Country(Resource):
    """ Resource for interacting with country records. """
    def get_path(self):
        return 'countries'


class Coupon(Resource):
    """ Resource for interacting with coupons records. """
    def get_path(self):
        return 'coupons'


class Customer(Resource):
    """ Resource for interacting with customer records. """
    def get_path(self):
        return 'customers'


class Deal(Resource):
    """ Resource for interacting with deal records. """
    def get_path(self):
        return 'deals'


class Department(Resource):
    """ Resource for interacting with company departments records. """
    def get_path(self):
        return 'company/departments'


class Directory(Resource):
    """ Resource for interacting with vendor/professional/intern directory records. """
    def get_path(self):
        return 'directory'


class Developer(Resource):
    """ Resource for interacting with developer records. """
    def get_path(self):
        return 'developers'


class Domain(Resource):
    """ Resource for interacting with domain records. """
    def get_path(self):
        return 'domains'


class Employee(Resource):
    """ Resource for interacting with company employee records. """
    def get_path(self):
        return 'company/employees'


class Finance(Resource):
    """ Resource for interacting with finance records. """
    def get_path(self):
        return 'finance'


class Group(Resource):
    """ Resource for interacting with group records records. """
    def get_path(self):
        return 'groups'


class Integration(Resource):
    """ Resource for interacting with external app integration records. """
    def get_path(self):
        return 'integrations'


class Invite(Resource):
    """ Resource for interacting with invite records. """
    def get_path(self):
        return 'invites'


class Location(Resource):
    """ Resource for interacting with company location (address) records. """
    def get_path(self):
        return 'company/locations'


class Order(Resource):
    """ Resource for interacting with order records. """
    def get_path(self):
        return 'orders'


class Partner(Resource):
    def get_path(self):
        return 'partners'


class Plan(Resource):
    """ Resource for interacting with plans records. """
    def requires_authorization(self):
        """ The request doesn't require authentication."""
        return False

    def get_path(self):
        return 'plans'


class Product(Resource):
    """ Resource for interacting with product records. """
    def get_path(self):
        return 'products'


class ProductCategory(Resource):
    """ Resource for interacting with product category records. """
    def get_path(self):
        return 'product-categories'


class State(Resource):
    """ Resource for interacting with state records. """
    def get_path(self):
        return 'states'


class Team(Resource):
    """ Resource for interacting with company team records. """
    def get_path(self):
        return 'company/teams'


class User(Resource):
    """ Resource for interacting with user records. """
    def get_path(self):
        return 'users'
