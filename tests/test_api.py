import logging

import pytest

from conftest import log_has
from pycwatch.errors import APIError
from pycwatch.rest import RestAPI


# TODO: this should be test_perform_request
def test_no_api_key(caplog):
    caplog.set_level(logging.INFO)
    api = RestAPI()
    line = "API Key needs to be set"
    with pytest.raises(APIError):
        assets = api.list_assets()
        assert log_has(line, caplog)


def test_key_setter():
    test_key = 'abcdefghijklmnopqrstuvwxyz'
    api = RestAPI()
    assert api.api_key is None
    assert 'X-CW-API-Key' not in list(api.client.headers)
    api.api_key = test_key
    assert api.api_key == test_key
    assert api.is_authenticated
    assert api.client.headers['X-CW-API-Key'] == test_key


def test_init_with_key():
    test_key = 'abcdefghijklmnopqrstuvwxyz'
    api = RestAPI(test_key)
    assert api.api_key == test_key
    assert api.is_authenticated
    assert api.client.headers['X-CW-API-Key'] == test_key
