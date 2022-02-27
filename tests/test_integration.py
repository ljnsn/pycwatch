"""Tests for the REST API methods."""
import json

from apiclient.exceptions import ClientError
import pytest
from vcr.cassette import Cassette

from .conftest import api_vcr
from pycwatch import CryptoWatchClient, models
from pycwatch.models import PaginatedResponse, Response
from pycwatch.errors import APIError, APIKeyError
from pycwatch.client import NO_KEY_MESSAGE
from pycwatch.endpoints import Endpoint


def with_cassette(cassette_file: str):
    def decorator(func):
        def wrapper(live_client, *args, **kwargs):
            with api_vcr.use_cassette(cassette_file) as cassette:
                result = func(cassette, live_client, *args, **kwargs)
            return result

        return wrapper

    return decorator


def load_response(cassette: Cassette, response_idx: int = 0):
    return json.loads(cassette.responses[response_idx]["body"]["string"])


def test_init_with_key(api_key):
    api = CryptoWatchClient(api_key)
    assert api._api_key == api_key
    assert api.is_authenticated


@with_cassette("list_assets.yml")
def test_list_assets(cassette: Cassette, live_client: CryptoWatchClient):
    assets = live_client.list_assets()
    assert assets == PaginatedResponse[models.AssetList](**load_response(cassette, 0))

    assets = live_client.list_assets(limit=20)
    assert assets == PaginatedResponse[models.AssetList](**load_response(cassette, 1))
    assert len(assets.result) == 20
    assert cassette.requests[1].uri == Endpoint.list_assets + "?limit=20"

    cursor = assets.cursor.last
    assets = live_client.list_assets(cursor=cursor, limit=20)
    assert assets == PaginatedResponse[models.AssetList](**load_response(cassette, 2))
    assert len(assets.result) == 20
    assert (
        cassette.requests[2].uri == Endpoint.list_assets + f"?cursor={cursor}&limit=20"
    )


@with_cassette("get_asset.yml")
def test_get_asset(cassette: Cassette, live_client: CryptoWatchClient):
    asset_codes = ["btc", "eur", "eth"]
    for i, asset_code in enumerate(asset_codes):
        asset = live_client.get_asset(asset_code=asset_code)
        assert asset == Response[models.Asset](**load_response(cassette, i))

    with pytest.raises(ClientError, match="404 Error: Not Found"):
        asset = live_client.get_asset(asset_code="aaa")


@with_cassette("list_pairs.yml")
def test_list_pairs(cassette: Cassette, live_client: CryptoWatchClient):
    pairs = live_client.list_pairs()
    assert pairs == PaginatedResponse[models.PairList](**load_response(cassette, 0))

    pairs = live_client.list_pairs(limit=20)
    assert pairs == PaginatedResponse[models.PairList](**load_response(cassette, 1))
    assert len(pairs.result) == 20
    assert cassette.requests[1].uri == Endpoint.list_pairs + "?limit=20"

    cursor = pairs.cursor.last
    pairs = live_client.list_pairs(cursor=cursor, limit=20)
    assert pairs == PaginatedResponse[models.PairList](**load_response(cassette, 2))
    assert len(pairs.result) == 20
    assert (
        cassette.requests[2].uri == Endpoint.list_pairs + f"?cursor={cursor}&limit=20"
    )


@with_cassette("get_pair.yml")
def test_get_pair(cassette: Cassette, live_client: CryptoWatchClient):
    pairs = ["btceur", "ethbtc", "xmrbtc"]
    for i, pair_ in enumerate(pairs):
        pair = live_client.get_pair(pair=pair_)
        assert pair == Response[models.Pair](**load_response(cassette, i))

    with pytest.raises(ClientError, match="404 Error: Not Found"):
        pair = live_client.get_pair(pair="aaa")


@with_cassette("list_exchanges")
def test_list_exchanges(cassette: Cassette, live_client: CryptoWatchClient):
    exchanges = live_client.list_exchanges()
    assert exchanges == Response[models.ExchangeList](**load_response(cassette, 0))


@with_cassette("get_exchange")
def test_get_exchange(cassette: Cassette, live_client: CryptoWatchClient):
    exchanges = ["kraken", "binance", "bittrex"]
    for i, ex in enumerate(exchanges):
        exchange = live_client.get_exchange(exchange=ex)
        assert exchange == Response[models.Exchange](**load_response(cassette, i))

    with pytest.raises(ClientError, match="404 Error: Not Found"):
        exchange = live_client.get_exchange(exchange="aaa")
