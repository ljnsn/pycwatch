from pycwatch import CryptoWatchClient


def test_init_with_key(api_key: str) -> None:
    """Verify that the client can be initialized with an API key."""
    api = CryptoWatchClient(api_key)
    assert api._api_key == api_key
    assert api.is_authenticated
