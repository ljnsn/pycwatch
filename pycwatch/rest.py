"""Provides the REST API class as well as all cryptowat.ch API resources"""
import requests
import urllib.parse

from pycwatch import resources
from pycwatch.errors import *


PRODUCTION_URL = 'https://api.cryptowat.ch{endpoint}'
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
        resource = resources.ListAssetsResource()
        return self.perform_request(resource)

    def get_asset_details(self, asset_code):
        resource = resources.AssetDetailsResource(asset_code)
        return self.perform_request(resource)

    def list_pairs(self):
        resource = resources.ListPairsResource()
        return self.perform_request(resource)

    def get_pair_details(self, pair):
        resource = resources.PairDetailsResource(pair)
        return self.perform_request(resource)

    def list_markets(self):
        resource = resources.ListMarketsResource()
        return self.perform_request(resource)

    def get_market_details(self, exchange, pair):
        resource = resources.MarketDetailsResource(exchange, pair)
        return self.perform_request(resource)

    def get_market_price(self, exchange, pair):
        resource = resources.MarketPriceResource(exchange, pair)
        return self.perform_request(resource)

    def get_all_market_prices(self):
        resource = resources.AllMarketPricesResource()
        return self.perform_request(resource)

    def get_market_trades(self, exchange, pair, since=None, limit=None):
        resource = resources.MarketTradesResource(exchange, pair, since, limit)
        return self.perform_request(resource)

    def get_market_summary(self, exchange, pair):
        resource = resources.MarketSummaryResource(exchange, pair)
        return self.perform_request(resource)

    def get_all_market_summaries(self, key_by=None):
        resource = resources.AllMarketSummariesResource(key_by)
        return self.perform_request(resource)

    def get_market_order_book(self, exchange, pair, depth=None, span=None,
                              limit=None):
        resource = resources.MarketOrderBookResource(exchange, pair, depth,
                                                     span, limit)
        return self.perform_request(resource)

    def get_market_order_book_liquidity(self, exchange, pair):
        resource = resources.MarketOrderBookLiquidityResource(exchange, pair)
        return self.perform_request(resource)

    def get_market_ohlc(self, exchange, pair, before=None, after=None,
                        periods=None, key_type='str'):
        if key_type not in ['str', 'int']:
            raise ValueError("`key_type` can be either 'str' or 'int'")
        resource = resources.MarketOHLCResource(exchange, pair, before, after,
                                                periods)
        response = self.perform_request(resource)
        if key_type == 'str':
            period_mapping_inv = {v: k for k, v in resources.PERIOD_VALUES.items()}
            return {period_mapping_inv[int(k)]: r for k, r in response.items()}
        return response

    def list_exchanges(self):
        resource = resources.ListExchangesResource()
        return self.perform_request(resource)

    def get_exchange_details(self, exchange):
        resource = resources.ExchangeDetailsResource(exchange)
        return self.perform_request(resource)

    def list_exchange_markets(self, exchange):
        resource = resources.ExchangeMarketsResource(exchange)
        return self.perform_request(resource)
