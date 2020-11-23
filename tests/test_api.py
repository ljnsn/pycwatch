import logging

import pytest

from conftest import log_has
from pycwatch.errors import APIError
from pycwatch.rest import RestAPI, KEY_HEADER


# TODO: this should be test_perform_request
def test_no_api_key(caplog):
    caplog.set_level(logging.INFO)
    api = RestAPI()
    line = "API Key needs to be set"
    with pytest.raises(APIError):
        assets = api.list_assets()
        assert log_has(line, caplog)


def test_key_setter(api_key):
    api = RestAPI()
    assert api.api_key is None
    assert KEY_HEADER not in list(api.client.headers)
    api.api_key = api_key
    assert api.api_key == api_key
    assert api.is_authenticated
    assert api.client.headers[KEY_HEADER] == api_key


def test_init_with_key(api_key):
    api = RestAPI(api_key)
    assert api.api_key == api_key
    assert api.is_authenticated
    assert api.client.headers[KEY_HEADER] == api_key
