import logging

import pytest
import requests_mock

from tests.conftest import log_has, register_resource
from pycwatch.errors import APIError
from pycwatch.rest import Allowance, RestAPI, KEY_HEADER


def test_key_setter(api_key):
    api = RestAPI()
    assert api.api_key is None
    assert KEY_HEADER not in list(api.client.headers)
    assert api.is_authenticated is False
    api.api_key = api_key
    assert api.api_key == api_key
    assert api.is_authenticated
    assert api.client.headers[KEY_HEADER] == api_key


def test_init_with_key(api_key):
    api = RestAPI(api_key)
    assert api.api_key == api_key
    assert api.is_authenticated
    assert api.client.headers[KEY_HEADER] == api_key


def test_perform_request_no_key(caplog, mock_resource):
    caplog.set_level(logging.INFO)
    api = RestAPI()
    line = "API Key needs to be set"
    with pytest.raises(APIError):
        api.perform_request(mock_resource)
        assert log_has(line, caplog)


@requests_mock.Mocker(kw='rmock')
def test_perform_request(mocker, api_key, mock_resource, **kwargs):
    api = RestAPI(api_key)
    mocker.patch("pycwatch.rest", api)
    resource = api.client.get_resource(mock_resource)
    response_expected = {
        "result": {
            "the-result": [1, 2, 3, 4, 5]
        }
    }
    update_allowance_mock = mocker.MagicMock()
    mocker.patch("pycwatch.rest.update_allowance", update_allowance_mock)
    register_resource(kwargs['rmock'], resource, 'GET', 200,
                      json=response_expected)
    result = api.perform_request(mock_resource)
    assert result == response_expected['result']
    update_allowance_mock.assert_called_once()


@requests_mock.Mocker(kw='rmock')
def test_update_allowance(mocker, api_key, mock_resource, **kwargs):
    api = RestAPI(api_key)
    mocker.patch("pycwatch.rest", api)
    resource = api.client.get_resource(mock_resource)
    response_expected = {
        "allowance": {
            "cost": 0.015,
            "remaining": 9.985,
            "upgrade": "Check https://cryptowat.ch"
        },
        "result": {}
    }
    allowance = Allowance(response_expected)
    register_resource(kwargs['rmock'], resource, 'GET', 200,
                      json=response_expected)
    assert api.allowance is None
    _ = api.perform_request(mock_resource)
    assert str(allowance) == str({
            'last_request_cost': 0.015,
            'remaining': 9.985,
            'remaining_paid': None
    })
    assert str(api.allowance) == str(allowance)
    assert api.allowance.cost == 0.015
    assert api.allowance.remaining == 9.985
