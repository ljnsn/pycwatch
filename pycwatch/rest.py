"""Provides the REST API class as well as all cryptowat.ch API resources"""
import requests
import urllib.parse

from pycwatch.errors import *


PRODUCTION_URL = 'https://api.cryptowat.ch{endpoint}'
PERIOD_VALUES = {
    '1m': 60,
    '3m': 180,
    '5m': 300,
    '15m': 900,
    '30m': 1800,
    '1h': 3600,
    '2h': 7200,
    '4h': 14400,
    '6h': 21600,
    '12h': 43200,
    '1d': 86400,
    '3d': 259200,
    '1w': 604800
}
KEY_HEADER = 'X-CW-API-Key'


class HTTPClient:
    DEFAULT_HEADERS = {
        'Accept': 'application/json',
        'Accept-Encoding': 'deflate, gzip'
    }
    raw_response = None

    def __init__(self, api_key, headers):
        header_apikey = {KEY_HEADER: api_key} if api_key else dict()
        headers = headers or dict()
        self.headers = {**self.DEFAULT_HEADERS, **headers, **header_apikey}

    def with_header(self, header, value):
        old_headers = self.headers
        new_header = {header: value}
        self.headers = {**old_headers, **new_header}

    def with_headers(self, additional_headers):
        old_headers = self.headers
        self.headers = {**old_headers, **additional_headers}

    @staticmethod
    def get_resource(resource):
        uri = PRODUCTION_URL.format(endpoint=resource.endpoint)
        if resource.query_parameters:
            query_string = urllib.parse.urlencode(resource.query_parameters)
            uri = '{}?{}'.format(uri, query_string)
        return uri

    def perform(self, resource):
        uri = self.get_resource(resource)

        raw_response = requests.get(uri, headers=self.headers)
        self.raw_response = raw_response
        if raw_response.status_code != 200:
            if hasattr(raw_response, 'json'):
                res = raw_response.json()
                exc = res.get('error', raw_response.text)
            else:
                exc = raw_response.text
            raise APIError(exc)
        return raw_response.json()


class Allowance:
    def __init__(self, response):
        allowance = response['allowance']
        self.cost = allowance['cost']
        self.remaining = allowance['remaining']
        self.remainingPaid = allowance.get('remainingPaid')
        self.upgrade = allowance.get('upgrade')
        self.account = allowance.get('upgrade')

    def __repr__(self):
        return str({
            'last_request_cost': self.cost,
            'remaining': self.remaining,
            'remaining_paid': self.remainingPaid
        })


class BaseResource:
    params = []

    @property
    def endpoint(self):
        raise NotImplementedError()

    @property
    def query_parameters(self):
        params = {}
        for param in self.params:
            if getattr(self, param):
                params[param] = getattr(self, param)
        return params


class ListAssetsResource(BaseResource):
    @property
    def endpoint(self):
        return '/assets'


class AssetDetailsResource(BaseResource):
    def __init__(self, asset_code):
        self.asset_code = asset_code

    @property
    def endpoint(self):
        return '/assets/{asset_code}'.format(asset_code=self.asset_code)


class ListPairsResource(BaseResource):
    @property
    def endpoint(self):
        return '/pairs'


class PairDetailsResource(BaseResource):
    def __init__(self, pair):
        self.pair = pair

    @property
    def endpoint(self):
        return '/pairs/{pair}'.format(pair=self.pair)


class ListMarketsResource(BaseResource):
    @property
    def endpoint(self):
        return '/markets'


class MarketDetailsResource(BaseResource):
    def __init__(self, exchange, pair):
        self.exchange = exchange
        self.pair = pair

    @property
    def endpoint(self):
        return '/markets/{exchange}/{pair}'.format(
            exchange=self.exchange, pair=self.pair
        )


class MarketPriceResource(BaseResource):
    def __init__(self, exchange, pair):
        self.exchange = exchange
        self.pair = pair

    @property
    def endpoint(self):
        return '/markets/{exchange}/{pair}/price'.format(
            exchange=self.exchange, pair=self.pair
        )


class AllMarketPricesResource(BaseResource):
    @property
    def endpoint(self):
        return '/markets/prices'


class MarketTradesResource(BaseResource):
    """
    Query Parameters
    ----------------
    since : integer
        Limit response to trades after this date (unix timestamp,
        Ex: 1589571417. NOTE: this can only be used to filter recent trades,
        not get historical trades
    limit : integer
        Limit the number of trades in the response. Max: 1000
    """
    params = ['since', 'limit']

    def __init__(self, exchange, pair, since=None, limit=None):
        self.exchange = exchange
        self.pair = pair
        self.since = since
        self.limit = limit

    @property
    def endpoint(self):
        return '/markets/{exchange}/{pair}/trades'.format(
            exchange=self.exchange, pair=self.pair
        )


class MarketSummaryResource(BaseResource):
    def __init__(self, exchange, pair):
        self.exchange = exchange
        self.pair = pair

    @property
    def endpoint(self):
        return '/markets/{exchange}/{pair}/summary'.format(
            exchange=self.exchange, pair=self.pair
        )


class AllMarketSummariesResource(BaseResource):
    """
    Query Parameters
    ----------------
    keyBy : string
        Values can be "id" or "symbols". This determines how each market
        object is indexed in the response.
    """
    params = ['keyBy']

    def __init__(self, key_by=None):
        self.keyBy = key_by

    @property
    def endpoint(self):
        return '/markets/summaries'


class MarketOrderBookResource(BaseResource):
    """
    Query Parameters
    ----------------
    depth : number
        Only return orders cumulating up to this size
    span : number
        Only return orders within this percentage of the midpoint.
        Example: 0.5 (meaning 0.5%)
    limit : integer
        Limits the number of orders on each side of the book
    """
    params = ['depth', 'span', 'limit']

    def __init__(self, exchange, pair, depth=None, span=None, limit=None):
        self.exchange = exchange
        self.pair = pair
        self.depth = depth
        self.span = span
        self.limit = limit

    @property
    def endpoint(self):
        return '/markets/{exchange}/{pair}/orderbook'.format(
            exchange=self.exchange, pair=self.pair
        )


class MarketOrderBookLiquidityResource(BaseResource):
    def __init__(self, exchange, pair):
        self.exchange = exchange
        self.pair = pair

    @property
    def endpoint(self):
        return '/markets/{exchange}/{pair}/orderbook/liquidity'.format(
            exchange=self.exchange, pair=self.pair
        )


class MarketOHLCResource(BaseResource):
    """
    Query Parameters
    ----------------
    before : integer
        Unix timestamp. Only return candles opening before this time.
        Example: 1481663244
    after : integer
        Unix timestamp. Only return candles opening after this time.
        Example 1481663244
    periods : array
        Comma separated integers. Only return these time periods.
        Example: 60,180,108000
    """
    params = ['before', 'after', 'periods']

    def __init__(self, exchange, pair, before=None, after=None, periods=None):
        self.exchange = exchange
        self.pair = pair
        self.before = before
        self.after = after
        self.periods = periods

    @property
    def endpoint(self):
        return '/markets/{exchange}/{pair}/ohlc'.format(
            exchange=self.exchange, pair=self.pair
        )


class ListExchangesResource(BaseResource):
    @property
    def endpoint(self):
        return '/exchanges'


class ExchangeDetailsResource(BaseResource):
    def __init__(self, exchange):
        self.exchange = exchange

    @property
    def endpoint(self):
        return '/exchanges/{exchange}'.format(exchange=self.exchange)


class ExchangeMarketsResource(BaseResource):
    def __init__(self, exchange):
        self.exchange = exchange

    @property
    def endpoint(self):
        return '/markets/{exchange}'.format(exchange=self.exchange)


class RestAPI:
    allowance = None

    def __init__(self, api_key=None, headers=None, client_class=HTTPClient):
        self._api_key = api_key
        self.client = client_class(api_key, headers)

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        if not api_key:
            raise APIKeyError("Please provide a valid API key")
        self._api_key = api_key
        self.client.with_header(KEY_HEADER, api_key)

    @property
    def is_authenticated(self):
        return self.api_key is not None

    def update_allowance(self, response):
        if 'allowance' in response:
            self.allowance = Allowance(response)

    def perform_request(self, resource):
        if not self.is_authenticated:
            raise APIError("API Key needs to be set")
        response = self.client.perform(resource)
        self.update_allowance(response)
        return response['result']

    def list_assets(self):
        resource = ListAssetsResource()
        return self.perform_request(resource)

    def get_asset_details(self, asset_code):
        resource = AssetDetailsResource(asset_code)
        return self.perform_request(resource)

    def list_pairs(self):
        resource = ListPairsResource()
        return self.perform_request(resource)

    def get_pair_details(self, pair):
        resource = PairDetailsResource(pair)
        return self.perform_request(resource)

    def list_markets(self):
        resource = ListMarketsResource()
        return self.perform_request(resource)

    def get_market_details(self, exchange, pair):
        resource = MarketDetailsResource(exchange, pair)
        return self.perform_request(resource)

    def get_market_price(self, exchange, pair):
        resource = MarketPriceResource(exchange, pair)
        return self.perform_request(resource)

    def get_all_market_prices(self):
        resource = AllMarketPricesResource()
        return self.perform_request(resource)

    def get_market_trades(self, exchange, pair, since=None, limit=None):
        resource = MarketTradesResource(exchange, pair, since, limit)
        return self.perform_request(resource)

    def get_market_summary(self, exchange, pair):
        resource = MarketSummaryResource(exchange, pair)
        return self.perform_request(resource)

    def get_all_market_summaries(self, key_by=None):
        resource = AllMarketSummariesResource(key_by)
        return self.perform_request(resource)

    def get_market_order_book(self, exchange, pair, depth=None, span=None,
                              limit=None):
        resource = MarketOrderBookResource(exchange, pair, depth, span, limit)
        return self.perform_request(resource)

    def get_market_order_book_liquidity(self, exchange, pair):
        resource = MarketOrderBookLiquidityResource(exchange, pair)
        return self.perform_request(resource)

    def get_market_ohlc(self, exchange, pair, before=None, after=None,
                        periods=None):
        # TODO: provide option to return period values or integers as keys
        if periods:
            if not isinstance(periods, list):
                periods = [periods]
            sec_periods = [
                str(PERIOD_VALUES[period]).lower() for period in periods
            ]
            periods = ','.join(sec_periods)
        resource = MarketOHLCResource(exchange, pair, before, after, periods)
        return self.perform_request(resource)

    def list_exchanges(self):
        resource = ListExchangesResource()
        return self.perform_request(resource)

    def get_exchange_details(self, exchange):
        resource = ExchangeDetailsResource(exchange)
        return self.perform_request(resource)

    def list_exchange_markets(self, exchange):
        resource = ExchangeMarketsResource(exchange)
        return self.perform_request(resource)
