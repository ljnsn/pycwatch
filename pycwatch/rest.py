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


class HTTPClient:
    DEFAULT_HEADERS = {
        'Accept': 'application/json',
        'Accept-Encoding': 'deflate, gzip'
    }
    raw_response = None

    def __init__(self, api_key, headers):
        header_apikey = {'X-CW-API-Key': api_key} if api_key else dict()
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
    def get_resource(request):
        resource = PRODUCTION_URL.format(endpoint=request.endpoint)
        if request.query_parameters:
            query_string = urllib.parse.urlencode(request.query_parameters)
            resource = '{}?{}'.format(resource, query_string)
        return resource

    def perform(self, request):
        resource = self.get_resource(request)

        raw_response = requests.get(resource, headers=self.headers)
        self.raw_response = raw_response
        if raw_response.status_code != 200:
            raise APIError()
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
        return {
            'last_request_cost': self.cost,
            'remaining': self.remaining,
            'remaining_paid': self.remainingPaid
        }


class BaseRequest:
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


class ListAssetsRequest(BaseRequest):
    @property
    def endpoint(self):
        return '/assets'


class AssetDetailsRequest(BaseRequest):
    def __init__(self, asset_code):
        self.asset_code = asset_code

    @property
    def endpoint(self):
        return '/assets/{asset_code}'.format(asset_code=self.asset_code)


class ListPairsRequest(BaseRequest):
    @property
    def endpoint(self):
        return '/pairs'


class PairDetailsRequest(BaseRequest):
    def __init__(self, pair):
        self.pair = pair

    @property
    def endpoint(self):
        return '/pairs/{pair}'.format(pair=self.pair)


class ListMarketsResource(BaseRequest):
    @property
    def endpoint(self):
        return '/markets'


class MarketDetailsRequest(BaseRequest):
    def __init__(self, exchange, pair):
        self.exchange = exchange
        self.pair = pair

    @property
    def endpoint(self):
        return '/markets/{exchange}/{pair}'.format(
            exchange=self.exchange, pair=self.pair
        )


class MarketPriceRequest(BaseRequest):
    def __init__(self, exchange, pair):
        self.exchange = exchange
        self.pair = pair

    @property
    def endpoint(self):
        return '/markets/{exchange}/{pair}/price'.format(
            exchange=self.exchange, pair=self.pair
        )


class AllMarketPricesRequest(BaseRequest):
    @property
    def endpoint(self):
        return '/markets/prices'


class MarketTradesRequest(BaseRequest):
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


class MarketSummaryRequest(BaseRequest):
    def __init__(self, exchange, pair):
        self.exchange = exchange
        self.pair = pair

    @property
    def endpoint(self):
        return '/markets/{exchange}/{pair}/summary'.format(
            exchange=self.exchange, pair=self.pair
        )


class AllMarketSummariesRequest(BaseRequest):
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


class MarketOrderBookRequest(BaseRequest):
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


class MarketOrderBookLiquidityRequest(BaseRequest):
    def __init__(self, exchange, pair):
        self.exchange = exchange
        self.pair = pair

    @property
    def endpoint(self):
        return '/markets/{exchange}/{pair}/orderbook/liquidity'.format(
            exchange=self.exchange, pair=self.pair
        )


class MarketOHLCRequest(BaseRequest):
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


class ListExchangesRequest(BaseRequest):
    @property
    def endpoint(self):
        return '/exchanges'


class ExchangeDetailsRequest(BaseRequest):
    def __init__(self, exchange):
        self.exchange = exchange

    @property
    def endpoint(self):
        return '/exchanges/{exchange}'.format(exchange=self.exchange)


class ExchangeMarketsRequest(BaseRequest):
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
        self.client.with_header("X-CW-API-Key", api_key)

    @property
    def is_authenticated(self):
        return self.api_key is not None

    def update_allowance(self, response):
        if 'allowance' in response:
            self.allowance = Allowance(response)

    def perform_request(self, request):
        if not self.is_authenticated:
            raise APIError("API Key needs to be set")
        response = self.client.perform(request)
        self.update_allowance(response)
        return response['result']

    def list_assets(self):
        request = ListAssetsRequest()
        return self.perform_request(request)

    def get_asset_details(self, asset_code):
        request = AssetDetailsRequest(asset_code)
        return self.perform_request(request)

    def list_pairs(self):
        request = ListPairsRequest()
        return self.perform_request(request)

    def get_pair_details(self, pair):
        request = PairDetailsRequest(pair)
        return self.perform_request(request)

    def list_markets(self):
        request = ListMarketsResource()
        return self.perform_request(request)

    def get_market_details(self, exchange, pair):
        request = MarketDetailsRequest(exchange, pair)
        return self.perform_request(request)

    def get_market_price(self, exchange, pair):
        request = MarketPriceRequest(exchange, pair)
        return self.perform_request(request)

    def get_all_market_prices(self):
        request = AllMarketPricesRequest()
        return self.perform_request(request)

    def get_market_trades(self, exchange, pair, since=None, limit=None):
        request = MarketTradesRequest(exchange, pair, since, limit)
        return self.perform_request(request)

    def get_market_summary(self, exchange, pair):
        request = MarketSummaryRequest(exchange, pair)
        return self.perform_request(request)

    def get_all_market_summaries(self, key_by=None):
        request = AllMarketSummariesRequest(key_by)
        return self.perform_request(request)

    def get_market_order_book(self, exchange, pair, depth=None, span=None,
                              limit=None):
        request = MarketOrderBookRequest(exchange, pair, depth, span, limit)
        return self.perform_request(request)

    def get_market_order_book_liquidity(self, exchange, pair):
        request = MarketOrderBookLiquidityRequest(exchange, pair)
        return self.perform_request(request)

    def get_market_ohlc(self, exchange, pair, before=None, after=None,
                        periods=None):
        if periods:
            if not isinstance(periods, list):
                periods = [periods]
            sec_periods = [
                str(PERIOD_VALUES[period]).lower() for period in periods
            ]
            periods = ','.join(sec_periods)
        request = MarketOHLCRequest(exchange, pair, before, after, periods)
        return self.perform_request(request)

    def list_exchanges(self):
        request = ListExchangesRequest()
        return self.perform_request(request)

    def get_exchange_details(self, exchange):
        request = ExchangeDetailsRequest(exchange)
        return self.perform_request(request)

    def list_exchange_markets(self, exchange):
        request = ExchangeMarketsRequest(exchange)
        return self.perform_request(request)
