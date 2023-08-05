import dorcas_sdk_python
import pytest


def test_response_representation():
    r = dorcas_sdk_python.DorcasResponse(dict(message='success', data=dict(numbers=[0, 1, 2, 3, 4]),
                                              errors=dict(message='There was a failure')))
    assert str(r) == "DorcasResponse<JSON={'message': 'success', 'data': {'numbers': [0, 1, 2, 3, 4]}, " \
                     "'errors': {'message': 'There was a failure'}}, http_status=200>"


def test_response_is_successful():
    r = dorcas_sdk_python.DorcasResponse(
        dict(message='success', data=dict(numbers=[0, 1, 2, 3, 4]), errors=dict(message='There was a failure')))
    assert r.is_successful() == True


def test_response_is_failure():
    r = dorcas_sdk_python.DorcasResponse(dict(message='error', errors=dict(message='Not found')), 404)
    assert False == r.is_successful()


def test_response_can_read_message():
    r = dorcas_sdk_python.DorcasResponse(
        dict(message='success', data=dict(numbers=[0, 1, 2, 3, 4]), errors=dict(message='There was a failure')))
    assert r.message() == 'success'


def test_response_can_read_error():
    r = dorcas_sdk_python.DorcasResponse(dict(message='error', errors=dict(message='Not Found')), 404)
    assert r.errors() is not None


def test_response_can_read_data():
    r = dorcas_sdk_python.DorcasResponse(
        dict(message='success', data=dict(numbers=[0, 1, 2, 3, 4]), errors=dict(message='There was a failure')))
    assert r.data is not None


def test_response_requires_json_dictionary():
    with pytest.raises(TypeError):
        dorcas_sdk_python.DorcasResponse('Not a dictionary')


def test_response_requires_int_http_status():
    with pytest.raises(TypeError):
        dorcas_sdk_python.DorcasResponse(dict(message='error', errors=dict(message='Not found')), 400.01)
