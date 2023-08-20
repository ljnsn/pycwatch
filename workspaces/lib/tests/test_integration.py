"""Tests for the REST API methods."""

import sys
from typing import Any, Callable, Dict, cast

if sys.version_info < (3, 10):
    from typing_extensions import Concatenate, ParamSpec
else:
    from typing import Concatenate, ParamSpec

import pytest
import ujson
from apiclient.exceptions import ClientError
from vcr.cassette import Cassette

from pycwatch.lib import CryptoWatchClient, models
from pycwatch.lib.conversion import converter
from pycwatch.lib.endpoints import Endpoint
from pycwatch.lib.models import PaginatedResponse, Response, ResponseRoot
from tests.conftest import api_vcr

P = ParamSpec("P")


def with_cassette(
    cassette_file: str,
) -> Callable[[Callable[P, None]], Callable[Concatenate[CryptoWatchClient, P], None]]:
    """Run a test with a VCR cassette."""

    def decorator(
        func: Callable[P, None]
    ) -> Callable[Concatenate[CryptoWatchClient, P], None]:
        def wrapper(
            live_client: CryptoWatchClient, *args: P.args, **kwargs: P.kwargs
        ) -> None:
            with api_vcr.use_cassette(cassette_file) as cassette:
                return func(cassette, live_client, *args, **kwargs)

        return wrapper

    return decorator


def load_response(cassette: Cassette, response_idx: int = 0) -> Dict[str, Any]:
    """Load a response from a VCR cassette."""
    response = ujson.loads(cassette.responses[response_idx]["body"]["string"])
    return cast(Dict[str, Any], response)


@with_cassette("get_info.yml")
def test_get_info(cassette: Cassette, live_client: CryptoWatchClient) -> None:
    """Verify that the get_info method returns the correct response."""
    response = live_client.get_info()

    assert response == converter.structure(
        load_response(cassette, 0),
        ResponseRoot[models.Info],
    )


@with_cassette("list_assets.yml")
def test_list_assets(cassette: Cassette, live_client: CryptoWatchClient) -> None:
    """Verify that the list_assets method returns the correct response."""
    assets = live_client.list_assets()
    assert assets == converter.structure(
        load_response(cassette, 0),
        PaginatedResponse[models.AssetList],
    )

    assets = live_client.list_assets(limit=20)
    assert assets == converter.structure(
        load_response(cassette, 1),
        PaginatedResponse[models.AssetList],
    )
    assert len(assets.result) == 20
    assert cassette.requests[1].uri == Endpoint.list_assets + "?limit=20"

    cursor = assets.cursor.last
    assets = live_client.list_assets(cursor=cursor, limit=20)
    assert assets == converter.structure(
        load_response(cassette, 2),
        PaginatedResponse[models.AssetList],
    )
    assert len(assets.result) == 20
    assert (
        cassette.requests[2].uri == Endpoint.list_assets + f"?cursor={cursor}&limit=20"
    )


@with_cassette("get_asset.yml")
def test_get_asset(cassette: Cassette, live_client: CryptoWatchClient) -> None:
    """Verify that the get_asset method returns the correct response."""
    asset_codes = ["btc", "eur", "eth", "kfee"]
    for i, asset_code in enumerate(asset_codes):
        asset = live_client.get_asset(asset_code=asset_code)
        assert asset == converter.structure(
            load_response(cassette, i),
            Response[models.Asset],
        )

    with pytest.raises(ClientError, match="404 Error: Not Found"):
        asset = live_client.get_asset(asset_code="does-not-exist")


@with_cassette("list_pairs.yml")
def test_list_pairs(cassette: Cassette, live_client: CryptoWatchClient) -> None:
    """Verify that the list_pairs method returns the correct response."""
    pairs = live_client.list_pairs()
    assert pairs == converter.structure(
        load_response(cassette, 0),
        PaginatedResponse[models.PairList],
    )

    pairs = live_client.list_pairs(limit=20)
    assert pairs == converter.structure(
        load_response(cassette, 1),
        PaginatedResponse[models.PairList],
    )
    assert len(pairs.result) == 20
    assert cassette.requests[1].uri == Endpoint.list_pairs + "?limit=20"

    cursor = pairs.cursor.last
    pairs = live_client.list_pairs(cursor=cursor, limit=20)
    assert pairs == converter.structure(
        load_response(cassette, 2),
        PaginatedResponse[models.PairList],
    )
    assert len(pairs.result) == 20
    assert (
        cassette.requests[2].uri == Endpoint.list_pairs + f"?cursor={cursor}&limit=20"
    )


@with_cassette("get_pair.yml")
def test_get_pair(cassette: Cassette, live_client: CryptoWatchClient) -> None:
    """Verify that the get_pair method returns the correct response."""
    pairs = ["btceur", "ethbtc", "xmrbtc"]
    for i, pair_ in enumerate(pairs):
        pair = live_client.get_pair(pair=pair_)
        assert pair == converter.structure(
            load_response(cassette, i),
            Response[models.Pair],
        )

    with pytest.raises(ClientError, match="404 Error: Not Found"):
        pair = live_client.get_pair(pair="does-not-exist")


@with_cassette("list_exchanges.yml")
def test_list_exchanges(cassette: Cassette, live_client: CryptoWatchClient) -> None:
    """Verify that the list_exchanges method returns the correct response."""
    exchanges = live_client.list_exchanges()
    assert exchanges == converter.structure(
        load_response(cassette, 0),
        Response[models.ExchangeList],
    )


@with_cassette("get_exchange.yml")
def test_get_exchange(cassette: Cassette, live_client: CryptoWatchClient) -> None:
    """Verify that the get_exchange method returns the correct response."""
    exchanges = ["kraken", "binance", "bittrex"]
    for i, ex in enumerate(exchanges):
        exchange = live_client.get_exchange(exchange=ex)
        assert exchange == converter.structure(
            load_response(cassette, i),
            Response[models.Exchange],
        )

    with pytest.raises(ClientError, match="404 Error: Not Found"):
        exchange = live_client.get_exchange(exchange="aaa")


@with_cassette("list_markets.yml")
def test_list_markets(cassette: Cassette, live_client: CryptoWatchClient) -> None:
    """Verify that the list_markets method returns the correct response."""
    markets = live_client.list_markets()
    assert markets == converter.structure(
        load_response(cassette, 0),
        PaginatedResponse[models.MarketList],
    )


@with_cassette("get_market.yml")
def test_get_market(cassette: Cassette, live_client: CryptoWatchClient) -> None:
    """Verify that the get_market method returns the correct response."""
    markets = [
        ("kraken", "btceur"),
        ("binance", "ethbtc"),
        ("kraken", "ltcbtc"),
        ("bittrex", "neoeth"),
    ]
    for i, m in enumerate(markets):
        market = live_client.get_market(exchange=m[0], pair=m[1])
        assert market == converter.structure(
            load_response(cassette, i),
            Response[models.Market],
        )

    with pytest.raises(ClientError, match="404 Error: Not Found"):
        market = live_client.get_market(exchange="kraken", pair="aaabbb")


@with_cassette("get_market_price.yml")
def test_get_market_price(cassette: Cassette, live_client: CryptoWatchClient) -> None:
    """Verify that the get_market_price method returns the correct response."""
    markets = [
        ("kraken", "btceur"),
        ("binance", "ethbtc"),
        ("kraken", "ltcbtc"),
        ("bittrex", "neoeth"),
    ]
    for i, m in enumerate(markets):
        price = live_client.get_market_price(exchange=m[0], pair=m[1])
        assert price == converter.structure(
            load_response(cassette, i),
            Response[models.MarketPrice],
        )

    with pytest.raises(ClientError, match="404 Error: Not Found"):
        price = live_client.get_market_price(exchange="kraken", pair="aaabbb")


@with_cassette("get_market_trades.yml")
def test_get_market_trades(cassette: Cassette, live_client: CryptoWatchClient) -> None:
    """Verify that the get_market_trades method returns the correct response."""
    markets = [
        ("kraken", "btceur"),
        ("binance", "ethbtc"),
        ("kraken", "ltcbtc"),
        ("bittrex", "neoeth"),
    ]
    for i, m in enumerate(markets):
        trades = live_client.get_market_trades(exchange=m[0], pair=m[1])
        assert trades == converter.structure(
            load_response(cassette, i),
            Response[models.MarketTradeList],
        )

    with pytest.raises(ClientError, match="404 Error: Not Found"):
        trades = live_client.get_market_trades(exchange="kraken", pair="aaabbb")


@with_cassette("get_market_summary.yml")
def test_get_market_summary(cassette: Cassette, live_client: CryptoWatchClient) -> None:
    """Verify that the get_market_summary method returns the correct response."""
    markets = [
        ("kraken", "btceur"),
        ("binance", "ethbtc"),
        ("kraken", "ltcbtc"),
        ("bittrex", "neoeth"),
    ]
    for i, m in enumerate(markets):
        summary = live_client.get_market_summary(exchange=m[0], pair=m[1])
        assert summary == converter.structure(
            load_response(cassette, i),
            Response[models.MarketSummary],
        )

    with pytest.raises(ClientError, match="404 Error: Not Found"):
        summary = live_client.get_market_summary(exchange="kraken", pair="aaabbb")


@with_cassette("get_market_order_book.yml")
def test_get_market_order_book(
    cassette: Cassette,
    live_client: CryptoWatchClient,
) -> None:
    """Verify that the get_market_order_book method returns the correct response."""
    markets = [
        ("kraken", "btceur"),
        ("binance", "ethbtc"),
        ("kraken", "ltcbtc"),
        ("bittrex", "neoeth"),
    ]
    for i, m in enumerate(markets):
        orderbook = live_client.get_market_order_book(exchange=m[0], pair=m[1])
        assert orderbook == converter.structure(
            load_response(cassette, i),
            Response[models.OrderBook],
        )

    with pytest.raises(ClientError, match="404 Error: Not Found"):
        orderbook = live_client.get_market_order_book(exchange="kraken", pair="aaabbb")


@with_cassette("get_market_order_book_liquidity.yml")
def test_get_market_order_book_liquidity(
    cassette: Cassette,
    live_client: CryptoWatchClient,
) -> None:
    """Verify that the method returns the correct response."""
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
        assert orderbook == converter.structure(
            load_response(cassette, i),
            Response[models.OrderBookLiquidity],
        )

    with pytest.raises(ClientError, match="404 Error: Not Found"):
        orderbook = live_client.get_market_order_book_liquidity(
            exchange="kraken", pair="aaabbb"
        )


@with_cassette("get_all_market_prices.yml")
def test_get_all_market_prices(
    cassette: Cassette,
    live_client: CryptoWatchClient,
) -> None:
    """Verify that the get_all_market_prices method returns the correct response."""
    prices = live_client.get_all_market_prices()
    assert prices == converter.structure(
        load_response(cassette, 0),
        PaginatedResponse[models.AllPrices],
    )


@with_cassette("get_all_market_summaries.yml")
def test_get_all_market_summaries(
    cassette: Cassette,
    live_client: CryptoWatchClient,
) -> None:
    """Verify that the get_all_market_summaries method returns the correct response."""
    summaries = live_client.get_all_market_summaries()
    assert summaries == converter.structure(
        load_response(cassette, 0),
        Response[models.AllSummaries],
    )


@with_cassette("calculate_quote.yml")
def test_calculate_quote(cassette: Cassette, live_client: CryptoWatchClient) -> None:
    """Verify that the calculate_quote method returns the correct response."""
    quote = live_client.calculate_quote(exchange="kraken", pair="btceur", amount=10)
    assert quote == converter.structure(
        load_response(cassette, 0),
        Response[models.OrderBookCalculator],
    )


@with_cassette("list_exchange_markets.yml")
def test_list_exchange_markets(
    cassette: Cassette,
    live_client: CryptoWatchClient,
) -> None:
    """Verify that the list_exchange_markets method returns the correct response."""
    exchanges = [
        "kraken",
        "binance",
        "kraken",
        "bittrex",
    ]
    for i, exchange in enumerate(exchanges):
        markets = live_client.list_exchange_markets(exchange=exchange)
        assert markets == converter.structure(
            load_response(cassette, i),
            Response[models.ExchangeMarkets],
        )

    with pytest.raises(ClientError, match="404 Error: Not Found"):
        markets = live_client.list_exchange_markets(exchange="aabbbaba")


@with_cassette("get_ohlcv.yml")
def test_get_ohlcv(cassette: Cassette, live_client: CryptoWatchClient) -> None:
    """Verify that the get_ohlcv method returns the correct response."""
    markets = [
        ("kraken", "btceur"),
        ("binance", "ethbtc"),
        ("kraken", "ltcbtc"),
        ("bittrex", "neoeth"),
    ]
    for i, m in enumerate(markets):
        ohlcv = live_client.get_ohlcv(exchange=m[0], pair=m[1])
        assert ohlcv == converter.structure(
            load_response(cassette, i),
            Response[models.OHLCVDict],
        )

    with pytest.raises(ClientError, match="404 Error: Not Found"):
        live_client.get_ohlcv(exchange="kraken", pair="aaabbb")
