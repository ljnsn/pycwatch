import attrs
import pytest
from apiclient.exceptions import ResponseParseError
from apiclient.response import Response
from pycwatch import CryptoWatchClient
from pycwatch.client import UJSONResponseHandler
from pycwatch.exceptions import ResponseStructureError
from pycwatch.models import ResponseRoot


def test_init_with_key(api_key: str) -> None:
    """Verify that the client can be initialized with an API key."""
    api = CryptoWatchClient(api_key)
    assert api._api_key == api_key
    assert api.is_authenticated


class FakeResponse(Response):
    """A fake response for testing."""

    def __init__(self, content: str) -> None:
        self.content = content

    def get_raw_data(self) -> str:
        """Return the raw data."""
        return self.content


def test_ujson_response_handler_no_data() -> None:
    """Verify an empty response returns None."""
    response = FakeResponse("")

    assert UJSONResponseHandler.get_request_data(response) is None


def test_ujson_response_handler_good_data() -> None:
    """Verify a good response is loaded correctly."""
    response = FakeResponse('{"foo": "bar"}')

    assert UJSONResponseHandler.get_request_data(response) == {"foo": "bar"}


def test_ujson_response_handler_bad_data() -> None:
    """Verify a malformed response raises an error."""
    response = FakeResponse("foo")

    with pytest.raises(ResponseParseError):
        UJSONResponseHandler.get_request_data(response)


def test_structuring_bad_response(live_client: CryptoWatchClient) -> None:
    """Verify attempting to structure a malformed response raises an error."""
    response = FakeResponse('{ "foo": "bar" }')

    @attrs.define()
    class ReponseCls:
        bar: str

    with pytest.raises(ResponseStructureError):
        live_client._structure_response(response, ResponseRoot[ReponseCls])
