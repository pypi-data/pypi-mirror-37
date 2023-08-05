import dorcas_sdk_python
import pytest
from dorcas_sdk_python.resources import Resource
from dorcas_sdk_python.services import Service


def test_sdk_default_environment():
    sdk = dorcas_sdk_python.Sdk()
    assert sdk.environment == 'staging'


def test_sdk_raises_error_for_non_string_client_id():
    with pytest.raises(TypeError):
        dorcas_sdk_python.Sdk(12345)


def test_sdk_raises_error_for_non_string_client_secret():
    with pytest.raises(TypeError):
        dorcas_sdk_python.Sdk('12345', 536437)


def test_sdk_sets_none_for_non_string_auth_token():
    sdk = dorcas_sdk_python.Sdk('id', 'secret', 12345)
    assert sdk.auth_token is None


def test_creates_resource_instance():
    sdk = dorcas_sdk_python.Sdk('id', 'secret')
    assert isinstance(sdk('resource', 'Advert'), Resource)


def test_creates_service_instance():
    sdk = dorcas_sdk_python.Sdk('id', 'secret')
    assert isinstance(sdk('service', 'Service'), Service)
