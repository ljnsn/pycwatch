"""Provides the REST API class as well as all cryptowat.ch API resources"""
import logging
import urllib.parse
from typing import Dict, Optional, Type

import requests

from pycwatch import resources
import pycwatch.errors


PRODUCTION_URL = "https://api.cryptowat.ch{endpoint}"
KEY_HEADER = "X-CW-API-Key"
NO_KEY_MESSAGE = """\
You have not set an API Key. Anonymous users are limited to 10 Cryptowatch \
Credits worth of API calls per 24-hour period.

See https://docs.cryptowat.ch/rest-api/rate-limit#api-request-pricing-structure \
for more information.\
"""


class HTTPClient:
    DEFAULT_HEADERS: Dict[str, str] = {
        "Accept": "application/json",
        "Accept-Encoding": "deflate, gzip",
    }
    raw_response: Optional[requests.Response] = None

    def __init__(self, api_key: Optional[str], headers: Optional[dict]) -> None:
        header_apikey = {KEY_HEADER: api_key} if api_key else dict()
        headers = headers or dict()
        self.headers = {**self.DEFAULT_HEADERS, **headers, **header_apikey}

    def with_header(self, header: str, value: str) -> None:
        old_headers = self.headers
        new_header = {header: value}
        self.headers = {**old_headers, **new_header}

    def with_headers(self, additional_headers: dict) -> None:
        old_headers = self.headers
        self.headers = {**old_headers, **additional_headers}

    @staticmethod
    def get_resource(resource: resources.Resource) -> str:
        uri = PRODUCTION_URL.format(endpoint=resource.endpoint)
        if resource.query_parameters:
            query_string = urllib.parse.urlencode(resource.query_parameters)
            uri = "{}?{}".format(uri, query_string)
        return uri

    def perform(self, resource: resources.Resource) -> dict:

        uri = self.get_resource(resource)
        raw_response = requests.get(uri, headers=self.headers)
        self.raw_response = raw_response

        if raw_response.status_code != 200:

            if hasattr(raw_response, "json"):

                res = raw_response.json()
                exc = res.get("error", raw_response.text)

            else:

                exc = raw_response.text

            raise pycwatch.errors.APIError(exc)

        return raw_response.json()


class Allowance:
    def __init__(self, response: dict) -> None:

        allowance = response["allowance"]
        self.cost = allowance["cost"]
        self.remaining = allowance["remaining"]
        self.remainingPaid = allowance.get("remainingPaid")
        self.upgrade = allowance.get("upgrade")
        self.account = allowance.get("upgrade")

    def __repr__(self) -> str:

        return str(
            {
                "last_request_cost": self.cost,
                "remaining": self.remaining,
                "remaining_paid": self.remainingPaid,
            }
        )


class RestAPI:
    """The interface to the cryptowat.ch Rest API.

    Provides methods to retrieve each available resource.
    """

    allowance: Optional[Allowance] = None

    def __init__(
        self,
        api_key: Optional[str] = None,
        headers: Optional[dict] = None,
        client_class: Type[HTTPClient] = HTTPClient,
    ) -> None:
        """Initialize the RestAPI class.

        Parameters
        ----------

        api_key : str or None, default None
            Your account's API key.

        headers : dict or None, default None
            A dictionary of extra headers you want to pass.

        client_class : type(HTTPClient), default `pycwatch.rest.HTTPClient`
            An HTTPClient class, possibly custom.
        """
        self._api_key = api_key
        self.client = client_class(api_key, headers)

    @property
    def api_key(self) -> Optional[str]:
        return self._api_key

    @api_key.setter
    def api_key(self, api_key: str) -> None:
        if not api_key:
            raise pycwatch.errors.APIKeyError("Please provide a valid API key")
        self._api_key = api_key
        self.client.with_header(KEY_HEADER, api_key)

    @property
    def is_authenticated(self) -> bool:
        return self.api_key is not None

    def _update_allowance(self, response: dict) -> None:
        if "allowance" in response:
            self.allowance = Allowance(response)

    def _perform_request(self, resource: resources.Resource) -> dict:
        if not self.is_authenticated:
            logging.debug(NO_KEY_MESSAGE)
        response = self.client.perform(resource)
        self._update_allowance(response)
        return response["result"]

    def list_assets(self):
        resource = resources.ListAssetsResource()
        return self._perform_request(resource)

    def get_asset_details(self, asset_code):
        resource = resources.AssetDetailsResource(asset_code)
        return self._perform_request(resource)

    def list_pairs(self):
        resource = resources.ListPairsResource()
        return self._perform_request(resource)

    def get_pair_details(self, pair):
        resource = resources.PairDetailsResource(pair)
        return self._perform_request(resource)

    def list_markets(self):
        resource = resources.ListMarketsResource()
        return self._perform_request(resource)

    def get_market_details(self, exchange, pair):
        resource = resources.MarketDetailsResource(exchange, pair)
        return self._perform_request(resource)

    def get_market_price(self, exchange, pair):
        resource = resources.MarketPriceResource(exchange, pair)
        return self._perform_request(resource)

    def get_all_market_prices(self):
        resource = resources.AllMarketPricesResource()
        return self._perform_request(resource)

    def get_market_trades(self, exchange, pair, since=None, limit=None):
        resource = resources.MarketTradesResource(exchange, pair, since, limit)
        return self._perform_request(resource)

    def get_market_summary(self, exchange, pair):
        resource = resources.MarketSummaryResource(exchange, pair)
        return self._perform_request(resource)

    def get_all_market_summaries(self, key_by=None):
        resource = resources.AllMarketSummariesResource(key_by)
        return self._perform_request(resource)

    def get_market_order_book(self, exchange, pair, depth=None, span=None, limit=None):
        resource = resources.MarketOrderBookResource(exchange, pair, depth, span, limit)
        return self._perform_request(resource)

    def get_market_order_book_liquidity(self, exchange, pair):
        resource = resources.MarketOrderBookLiquidityResource(exchange, pair)
        return self._perform_request(resource)

    def get_market_ohlc(
        self,
        exchange,
        pair,
        before=None,
        after=None,
        periods=None,
        result_key_type="str",
    ):

        if result_key_type not in ["str", "int"]:
            raise ValueError("`key_type' can be either 'str' or 'int'")

        resource = resources.MarketOHLCResource(exchange, pair, before, after, periods)

        response = self._perform_request(resource)

        # FIXME: should we convert the response key to int?
        if result_key_type == "str":
            period_mapping_inv = {v: k for k, v in resources.PERIOD_VALUES.items()}
            return {period_mapping_inv[int(k)]: r for k, r in response.items()}

        return response

    def list_exchanges(self):
        resource = resources.ListExchangesResource()
        return self._perform_request(resource)

    def get_exchange_details(self, exchange):
        resource = resources.ExchangeDetailsResource(exchange)
        return self._perform_request(resource)

    def list_exchange_markets(self, exchange):
        resource = resources.ExchangeMarketsResource(exchange)
        return self._perform_request(resource)
