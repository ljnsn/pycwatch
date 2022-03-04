"""Tests for the REST API methods."""
import json

import pytest
from apiclient.exceptions import ClientError
from vcr.cassette import Cassette

from pycwatch import CryptoWatchClient, models
from pycwatch.endpoints import Endpoint
from pycwatch.models import PaginatedResponse, Response

from .conftest import api_vcr


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


@with_cassette("list_exchanges.yml")
def test_list_exchanges(cassette: Cassette, live_client: CryptoWatchClient):
    exchanges = live_client.list_exchanges()
    assert exchanges == Response[models.ExchangeList](**load_response(cassette, 0))


@with_cassette("get_exchange.yml")
def test_get_exchange(cassette: Cassette, live_client: CryptoWatchClient):
    exchanges = ["kraken", "binance", "bittrex"]
    for i, ex in enumerate(exchanges):
        exchange = live_client.get_exchange(exchange=ex)
        assert exchange == Response[models.Exchange](**load_response(cassette, i))

    with pytest.raises(ClientError, match="404 Error: Not Found"):
        exchange = live_client.get_exchange(exchange="aaa")


@with_cassette("list_markets.yml")
def test_list_markets(cassette: Cassette, live_client: CryptoWatchClient):
    markets = live_client.list_markets()
    assert markets == PaginatedResponse[models.MarketList](**load_response(cassette, 0))


@with_cassette("get_market.yml")
def test_get_market(cassette: Cassette, live_client: CryptoWatchClient):
    markets = [
        ("kraken", "btceur"),
        ("binance", "ethbtc"),
        ("kraken", "ltcbtc"),
        ("bittrex", "neoeth"),
    ]
    for i, m in enumerate(markets):
        market = live_client.get_market(exchange=m[0], pair=m[1])
        assert market == Response[models.Market](**load_response(cassette, i))

    with pytest.raises(ClientError, match="404 Error: Not Found"):
        market = live_client.get_market(exchange="kraken", pair="aaabbb")


@with_cassette("get_market_price.yml")
def test_get_market_price(cassette: Cassette, live_client: CryptoWatchClient):
    markets = [
        ("kraken", "btceur"),
        ("binance", "ethbtc"),
        ("kraken", "ltcbtc"),
        ("bittrex", "neoeth"),
    ]
    for i, m in enumerate(markets):
        price = live_client.get_market_price(exchange=m[0], pair=m[1])
        assert price == Response[models.MarketPrice](**load_response(cassette, i))

    with pytest.raises(ClientError, match="404 Error: Not Found"):
        price = live_client.get_market_price(exchange="kraken", pair="aaabbb")


@with_cassette("get_market_trades.yml")
def test_get_market_trades(cassette: Cassette, live_client: CryptoWatchClient):
    markets = [
        ("kraken", "btceur"),
        ("binance", "ethbtc"),
        ("kraken", "ltcbtc"),
        ("bittrex", "neoeth"),
    ]
    for i, m in enumerate(markets):
        trades = live_client.get_market_trades(exchange=m[0], pair=m[1])
        assert trades == Response[models.MarketTradeList](**load_response(cassette, i))

    with pytest.raises(ClientError, match="404 Error: Not Found"):
        trades = live_client.get_market_trades(exchange="kraken", pair="aaabbb")


@with_cassette("get_market_summary.yml")
def test_get_market_summary(cassette: Cassette, live_client: CryptoWatchClient):
    markets = [
        ("kraken", "btceur"),
        ("binance", "ethbtc"),
        ("kraken", "ltcbtc"),
        ("bittrex", "neoeth"),
    ]
    for i, m in enumerate(markets):
        summary = live_client.get_market_summary(exchange=m[0], pair=m[1])
        assert summary == Response[models.MarketSummary](**load_response(cassette, i))

    with pytest.raises(ClientError, match="404 Error: Not Found"):
        summary = live_client.get_market_summary(exchange="kraken", pair="aaabbb")


@with_cassette("get_market_order_book.yml")
def test_get_market_order_book(cassette: Cassette, live_client: CryptoWatchClient):
    markets = [
        ("kraken", "btceur"),
        ("binance", "ethbtc"),
        ("kraken", "ltcbtc"),
        ("bittrex", "neoeth"),
    ]
    for i, m in enumerate(markets):
        orderbook = live_client.get_market_order_book(exchange=m[0], pair=m[1])
        assert orderbook == Response[models.OrderBook](**load_response(cassette, i))

    with pytest.raises(ClientError, match="404 Error: Not Found"):
        orderbook = live_client.get_market_order_book(exchange="kraken", pair="aaabbb")


@with_cassette("get_market_order_book_liquidity.yml")
def test_get_market_order_book_liquidity(
    cassette: Cassette, live_client: CryptoWatchClient
):
    markets = [
        ("kraken", "btceur"),
        ("binance", "ethbtc"),
        ("kraken", "ltcbtc"),
        ("bittrex", "neoeth"),
    ]
    for i, m in enumerate(markets):
        orderbook = live_client.get_market_order_book_liquidity(
            exchange=m[0], pair=m[1]
        )
        assert orderbook == Response[models.OrderBookLiquidity](
            **load_response(cassette, i)
        )

    with pytest.raises(ClientError, match="404 Error: Not Found"):
        orderbook = live_client.get_market_order_book_liquidity(
            exchange="kraken", pair="aaabbb"
        )


@with_cassette("get_all_market_prices.yml")
def test_get_all_market_prices(cassette: Cassette, live_client: CryptoWatchClient):
    prices = live_client.get_all_market_prices()
    assert prices == PaginatedResponse[models.AllPrices](**load_response(cassette, 0))


@with_cassette("get_all_market_summaries.yml")
def test_get_all_market_summaries(cassette: Cassette, live_client: CryptoWatchClient):
    summaries = live_client.get_all_market_summaries()
    assert summaries == Response[models.AllSummaries](**load_response(cassette))


@with_cassette("calculate_quote.yml")
def test_calculate_quote(cassette: Cassette, live_client: CryptoWatchClient):
    quote = live_client.calculate_quote(exchange="kraken", pair="btceur", amount=10)
    assert quote == Response[models.OrderBookCalculator](**load_response(cassette, 0))


@with_cassette("list_exchange_markets.yml")
def test_list_exchange_markets(cassette: Cassette, live_client: CryptoWatchClient):
    exchanges = [
        "kraken",
        "binance",
        "kraken",
        "bittrex",
    ]
    for i, exchange in enumerate(exchanges):
        markets = live_client.list_exchange_markets(exchange=exchange)
        assert markets == Response[models.ExchangeMarkets](**load_response(cassette, i))

    with pytest.raises(ClientError, match="404 Error: Not Found"):
        markets = live_client.list_exchange_markets(exchange="aabbbaba")


@with_cassette("get_ohlcv.yml")
def test_get_ohlcv(cassette: Cassette, live_client: CryptoWatchClient):
    markets = [
        ("kraken", "btceur"),
        ("binance", "ethbtc"),
        ("kraken", "ltcbtc"),
        ("bittrex", "neoeth"),
    ]
    for i, m in enumerate(markets):
        ohlcv = live_client.get_ohlcv(exchange=m[0], pair=m[1])
        assert ohlcv == Response[models.OHLCVDict](**load_response(cassette, i))

    with pytest.raises(ClientError, match="404 Error: Not Found"):
        ohlcv = live_client.get_ohlcv(exchange="kraken", pair="aaabbb")
