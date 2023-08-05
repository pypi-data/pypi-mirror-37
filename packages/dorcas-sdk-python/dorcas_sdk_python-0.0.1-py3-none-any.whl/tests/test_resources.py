import dorcas_sdk_python
from dorcas_sdk_python.resources import Resource, Advert, Application, AppStore, Blog, Company, ContactField, Country, \
    Coupon, Customer, Deal, Department, Directory, Developer, Domain, Employee, Finance, Group, Integration, \
    Invite, Location, Order, Partner, Plan, Product, ProductCategory, State, Team, User
import pytest

sdk = dorcas_sdk_python.Sdk()


def test_sdk_creates_resource_advert():
    resource = sdk('resource', 'Advert')
    assert isinstance(resource, Advert)
    assert isinstance(resource, Resource)


def test_sdk_creates_resource_developer_application():
    resource = sdk('resource', 'Application')
    assert isinstance(resource, Application)
    assert isinstance(resource, Resource)


def test_sdk_creates_resource_app_store():
    resource = sdk('resource', 'AppStore')
    assert isinstance(resource, AppStore)
    assert isinstance(resource, Resource)
    with pytest.raises(dorcas_sdk_python.DorcasException):
        assert resource.validate_payload()
    resource.add_query_param('oauth_client', 'fake client id')
    assert resource.validate_payload()


def test_sdk_creates_resource_blog():
    resource = sdk('resource', 'Blog')
    assert isinstance(resource, Blog)
    assert isinstance(resource, Resource)


def test_sdk_creates_resource_company():
    resource = sdk('resource', 'Company')
    assert isinstance(resource, Company)
    assert isinstance(resource, Resource)


def test_sdk_creates_resource_contact_field():
    resource = sdk('resource', 'ContactField')
    assert isinstance(resource, ContactField)
    assert isinstance(resource, Resource)


def test_sdk_creates_resource_coupon():
    resource = sdk('resource', 'Coupon')
    assert isinstance(resource, Coupon)
    assert isinstance(resource, Resource)


def test_sdk_creates_resource_country():
    resource = sdk('resource', 'Country')
    assert isinstance(resource, Country)
    assert isinstance(resource, Resource)


def test_sdk_creates_resource_customer():
    resource = sdk('resource', 'Customer')
    assert isinstance(resource, Customer)
    assert isinstance(resource, Resource)


def test_sdk_creates_resource_deal():
    resource = sdk('resource', 'Deal')
    assert isinstance(resource, Deal)
    assert isinstance(resource, Resource)


def test_sdk_creates_resource_department():
    resource = sdk('resource', 'Department')
    assert isinstance(resource, Department)
    assert isinstance(resource, Resource)


def test_sdk_creates_resource_directory():
    resource = sdk('resource', 'Directory')
    assert isinstance(resource, Directory)
    assert isinstance(resource, Resource)


def test_sdk_creates_resource_developer():
    resource = sdk('resource', 'Developer')
    assert isinstance(resource, Developer)
    assert isinstance(resource, Resource)


def test_sdk_creates_resource_domain():
    resource = sdk('resource', 'Domain')
    assert isinstance(resource, Domain)
    assert isinstance(resource, Resource)


def test_sdk_creates_resource_employee():
    resource = sdk('resource', 'Employee')
    assert isinstance(resource, Employee)
    assert isinstance(resource, Resource)


def test_sdk_creates_resource_finance():
    resource = sdk('resource', 'Finance')
    assert isinstance(resource, Finance)
    assert isinstance(resource, Resource)


def test_sdk_creates_resource_group():
    resource = sdk('resource', 'Group')
    assert isinstance(resource, Group)
    assert isinstance(resource, Resource)


def test_sdk_creates_resource_integration():
    resource = sdk('resource', 'Integration')
    assert isinstance(resource, Integration)
    assert isinstance(resource, Resource)


def test_sdk_creates_resource_invite():
    resource = sdk('resource', 'Invite')
    assert isinstance(resource, Invite)
    assert isinstance(resource, Resource)


def test_sdk_creates_resource_location():
    resource = sdk('resource', 'Location')
    assert isinstance(resource, Location)
    assert isinstance(resource, Resource)


def test_sdk_creates_resource_order():
    resource = sdk('resource', 'Order')
    assert isinstance(resource, Order)
    assert isinstance(resource, Resource)


def test_sdk_creates_resource_partner():
    resource = sdk('resource', 'Partner')
    assert isinstance(resource, Partner)
    assert isinstance(resource, Resource)


def test_sdk_creates_resource_plan():
    resource = sdk('resource', 'Plan')
    assert isinstance(resource, Plan)
    assert isinstance(resource, Resource)


def test_sdk_creates_resource_product():
    resource = sdk('resource', 'Product')
    assert isinstance(resource, Product)
    assert isinstance(resource, Resource)


def test_sdk_creates_resource_product_categories():
    resource = sdk('resource', 'ProductCategory')
    assert isinstance(resource, ProductCategory)
    assert isinstance(resource, Resource)


def test_sdk_creates_resource_state():
    resource = sdk('resource', 'State')
    assert isinstance(resource, State)
    assert isinstance(resource, Resource)


def test_sdk_creates_resource_team():
    resource = sdk('resource', 'Team')
    assert isinstance(resource, Team)
    assert isinstance(resource, Resource)


def test_sdk_creates_resource_user():
    resource = sdk('resource', 'User')
    assert isinstance(resource, User)
    assert isinstance(resource, Resource)
