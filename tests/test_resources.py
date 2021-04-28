"""Tests for each individual resource."""
from pycwatch import resources


def test_base_resource():
    resource = resources.BaseResource()
    resource.endpoint == NotImplemented
    assert resource.query_parameters == dict()
    resource.params = ['param1', 'param2']
    resource.param1 = 'val1'
    resource.param2 = 'val2'
    assert resource.query_parameters == {'param1': 'val1', 'param2': 'val2'}


def test_list_assets_resource():
    resource = resources.ListAssetsResource()
    assert resource.endpoint == '/assets'
    assert resource.params == []
    assert resource.query_parameters == {}


def test_asset_details_resource():
    asset_code = 'eur'
    resource = resources.AssetDetailsResource(asset_code)
    assert resource.asset_code == asset_code
    assert resource.endpoint == '/assets/eur'
    assert resource.params == []
    assert resource.query_parameters == {}


def test_list_pairs_resource():
    resource = resources.ListPairsResource()
    assert resource.endpoint == '/pairs'
    assert resource.params == []
    assert resource.query_parameters == {}


def test_pair_details_resource():
    pair = 'btceur'
    resource = resources.PairDetailsResource(pair)
    assert resource.pair == pair
    assert resource.endpoint == '/pairs/btceur'
    assert resource.params == []
    assert resource.query_parameters == {}


def test_list_markets_resource():
    resource = resources.ListMarketsResource()
    assert resource.endpoint == '/markets'
    assert resource.params == []
    assert resource.query_parameters == {}


def test_market_details_resource():
    exchange = 'binance'
    pair = 'btceur'
    resource = resources.MarketDetailsResource(exchange, pair)
    assert resource.exchange == exchange
    assert resource.pair == pair
    assert resource.endpoint == '/markets/binance/btceur'
    assert resource.params == []
    assert resource.query_parameters == {}


def test_market_price_resource():
    exchange = 'binance'
    pair = 'btceur'
    resource = resources.MarketPriceResource(exchange, pair)
    assert resource.exchange == exchange
    assert resource.pair == pair
    assert resource.endpoint == '/markets/binance/btceur/price'
    assert resource.params == []
    assert resource.query_parameters == {}


def test_all_market_prices_resource():
    resource = resources.AllMarketPricesResource()
    assert resource.endpoint == '/markets/prices'
    assert resource.params == []
    assert resource.query_parameters == {}


def test_market_trades_resource():
    exchange = 'binance'
    pair = 'btceur'
    resource = resources.MarketTradesResource(exchange, pair)
    assert resource.endpoint == '/markets/binance/btceur/trades'
    assert resource.params == ['since', 'limit']
    assert resource.query_parameters == {}
    assert resource.exchange == exchange
    assert resource.pair == pair
    assert resource.since is None
    assert resource.limit is None
    since, limit = 100, 1000
    resource = resources.MarketTradesResource(exchange, pair, since, limit)
    assert resource.endpoint == '/markets/binance/btceur/trades'
    assert resource.since == since
    assert resource.limit == limit
    assert resource.query_parameters == {'since': since, 'limit': limit}


def test_market_summary_resource():
    exchange = 'binance'
    pair = 'btceur'
    resource = resources.MarketSummaryResource(exchange, pair)
    assert resource.endpoint == '/markets/binance/btceur/summary'
    assert resource.exchange == exchange
    assert resource.pair == pair
    assert resource.params == []
    assert resource.query_parameters == {}


def test_all_market_summary_resource():
    resource = resources.AllMarketSummariesResource()
    assert resource.endpoint == '/markets/summaries'
    assert resource.params == ['keyBy']
    assert resource.keyBy is None
    assert resource.query_parameters == {}
    resource = resources.AllMarketSummariesResource(key_by='id')
    assert resource.endpoint == '/markets/summaries'
    assert resource.keyBy == 'id'
    assert resource.query_parameters == dict(keyBy='id')


def test_market_order_book_resource():
    exchange = 'binance'
    pair = 'btceur'
    resource = resources.MarketOrderBookResource(exchange, pair)
    assert resource.endpoint == '/markets/binance/btceur/orderbook'
    assert resource.params == ['depth', 'span', 'limit']
    assert resource.query_parameters == {}
    assert resource.exchange == exchange
    assert resource.pair == pair
    assert resource.depth is None
    assert resource.span is None
    assert resource.limit is None
    depth, span, limit = 1, .5, 10
    resource = resources.MarketOrderBookResource(exchange, pair, depth, span,
                                                 limit)
    assert resource.endpoint == '/markets/binance/btceur/orderbook'
    assert resource.depth == depth
    assert resource.span == span
    assert resource.limit == limit
    assert resource.query_parameters == dict(depth=depth, span=span,
                                             limit=limit)


def test_market_order_book_liquidity_resource():
    exchange = 'binance'
    pair = 'btceur'
    resource = resources.MarketOrderBookLiquidityResource(exchange, pair)
    assert resource.endpoint == '/markets/binance/btceur/orderbook/liquidity'
    assert resource.exchange == exchange
    assert resource.pair == pair
    assert resource.params == []
    assert resource.query_parameters == {}


def test_market_ohlc_resource():
    exchange = 'binance'
    pair = 'btceur'
    resource = resources.MarketOHLCResource(exchange, pair)
    assert resource.endpoint == '/markets/binance/btceur/ohlc'
    assert resource.params == ['before', 'after', 'periods']
    assert resource.query_parameters == {}
    assert resource.exchange == exchange
    assert resource.pair == pair
    assert resource.before is None
    assert resource.after is None
    assert resource.periods is None
    before, after, periods = 1000, 2000, ['1m', '3m', '30m', 60]
    sec_periods = ','.join([
        str(resources.PERIOD_VALUES[period.lower()])
        if isinstance(period, str) else str(period) for period in periods
    ])
    resource = resources.MarketOHLCResource(exchange, pair, before, after,
                                            periods)
    assert resource.endpoint == '/markets/binance/btceur/ohlc'
    assert resource.before == before
    assert resource.after == after
    assert resource.periods == sec_periods
    assert resource.query_parameters == dict(before=before, after=after,
                                             periods=sec_periods)


def test_list_exchanges_resource():
    resource = resources.ListExchangesResource()
    assert resource.endpoint == '/exchanges'
    assert resource.params == []
    assert resource.query_parameters == {}


def test_exchange_details_resource():
    exchange = 'binance'
    resource = resources.ExchangeDetailsResource(exchange)
    assert resource.endpoint == '/exchanges/binance'
    assert resource.exchange == exchange
    assert resource.params == []
    assert resource.query_parameters == {}


def test_exchange_markets_resource():
    exchange = 'binance'
    resource = resources.ExchangeMarketsResource(exchange)
    assert resource.endpoint == '/markets/binance'
    assert resource.exchange == exchange
    assert resource.params == []
    assert resource.query_parameters == {}
