import dorcas_sdk_python
from dorcas_sdk_python.services import Service, Authorization, Company, PasswordLogin, Metrics, Profile, \
    Registration, Store
import pytest

sdk = dorcas_sdk_python.Sdk()


def test_sdk_creates_service_authorization():
    resource = sdk('service', 'Authorization')
    assert isinstance(resource, Authorization)
    assert isinstance(resource, Service)


def test_sdk_creates_service_company():
    resource = sdk('service', 'Company')
    assert isinstance(resource, Company)
    assert isinstance(resource, Service)


def test_sdk_creates_service_metrics():
    resource = sdk('service', 'Metrics')
    assert isinstance(resource, Metrics)
    assert isinstance(resource, Service)


def test_sdk_creates_service_password_login():
    resource = sdk('service', 'PasswordLogin')
    assert isinstance(resource, PasswordLogin)
    assert isinstance(resource, Service)


def test_sdk_creates_service_profile():
    resource = sdk('service', 'Profile')
    assert isinstance(resource, Profile)
    assert isinstance(resource, Service)


def test_sdk_creates_service_registration():
    resource = sdk('service', 'Registration')
    assert isinstance(resource, Registration)
    assert isinstance(resource, Service)
    with pytest.raises(dorcas_sdk_python.DorcasException):
        assert resource.validate_payload()
    resource.body.set_items(dict(email='fake@gmail.com', password='password', firstname='firstname',
                                 lastname='lastname', phone='08123456789', company='Company Name'))
    with pytest.raises(dorcas_sdk_python.DorcasException):
        assert resource.validate_payload()
    resource.prefill_body()
    assert resource.validate_payload()


def test_sdk_creates_service_store():
    resource = sdk('service', 'Store')
    assert isinstance(resource, Store)
    assert isinstance(resource, Service)
