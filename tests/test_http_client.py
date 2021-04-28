"""Tests for the HTTP client."""
import pytest
import requests
import requests_mock

from tests.conftest import log_has, register_resource
from pycwatch.errors import APIError
from pycwatch.rest import HTTPClient, KEY_HEADER, PRODUCTION_URL


def test_client():
    client = HTTPClient(api_key=None, headers=None)
    assert client.headers == client.DEFAULT_HEADERS


def test_client_with_key():
    client = HTTPClient(api_key="test-key", headers=None)
    headers = {**client.DEFAULT_HEADERS, KEY_HEADER: "test-key"}
    assert client.headers == headers


def test_client_with_headers():
    test_headers = {'test-header1': 'test-value1',
                    'test-header2': 'test-value2'}
    client = HTTPClient(api_key=None, headers=test_headers)
    headers = {**client.DEFAULT_HEADERS, **test_headers}
    assert client.headers == headers


def test_with_header(http_client):
    test_key, test_value = 'test-key', 'test-value'
    http_client.with_header(test_key, test_value)
    headers = {**http_client.DEFAULT_HEADERS, test_key: test_value}
    assert http_client.headers == headers


def test_with_headers(http_client):
    test_headers = {'test-header1': 'test-value1',
                    'test-header2': 'test-value2'}
    http_client.with_headers(test_headers)
    headers = {**http_client.DEFAULT_HEADERS, **test_headers}
    assert http_client.headers == headers


def test_get_resource(http_client, mock_resource):
    base_url = PRODUCTION_URL.format(endpoint="/path/test-part")
    resource_expected = base_url + "?param=test-value"
    resource = http_client.get_resource(mock_resource)
    assert resource == resource_expected
 

@requests_mock.Mocker(kw='rmock')
def test_perform_good_response(http_client, mock_resource, **kwargs):
    resource = http_client.get_resource(mock_resource)
    response_expected = {'a': 2}
    register_resource(kwargs['rmock'], resource, 'GET', 200,
                      json=response_expected)
    assert http_client.raw_response is None
    response = http_client.perform(mock_resource)
    assert response == response_expected
    assert isinstance(http_client.raw_response, requests.models.Response)


@requests_mock.Mocker(kw='rmock')
def test_perform_bad_response(http_client, mock_resource, caplog, **kwargs):
    resource = http_client.get_resource(mock_resource)
    response_expected = {"error": "Route not found"}
    register_resource(kwargs['rmock'], resource, 'GET', 404,
                      json=response_expected)
    assert http_client.raw_response is None
    with pytest.raises(APIError):
        response = http_client.perform(mock_resource)
        assert response == response_expected
        assert isinstance(http_client.raw_response, requests.models.Response)
        assert log_has(response.text, caplog)
