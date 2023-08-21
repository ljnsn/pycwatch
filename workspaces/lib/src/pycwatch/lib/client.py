"""The module that holds the API client."""

from typing import Any, List, Optional, Type, TypeVar, Union

import attrs
import cattrs
import ujson
from apiclient import APIClient
from apiclient.authentication_methods import HeaderAuthentication, NoAuthentication
from apiclient.exceptions import ResponseParseError
from apiclient.response import Response as APIClientResponse
from apiclient.response_handlers import BaseResponseHandler
from apiclient.utils.typing import JsonType

from pycwatch.lib.config import settings
from pycwatch.lib.conversion import converter
from pycwatch.lib.endpoints import Endpoint
from pycwatch.lib.exceptions import ResponseStructureError
from pycwatch.lib.models import (
    AllPrices,
    AllSummaries,
    Asset,
    AssetList,
    Exchange,
    ExchangeList,
    ExchangeMarkets,
    Info,
    Market,
    MarketList,
    MarketPrice,
    MarketSummariesQueryParams,
    MarketSummary,
    MarketTradeList,
    OHLCVDict,
    OHLCVQueryParams,
    OrderBook,
    OrderBookCalculator,
    OrderBookCalculatorQueryParams,
    OrderBookLiquidity,
    OrderBookQueryParams,
    PaginatedResponse,
    PaginationQueryParams,
    Pair,
    PairList,
    Response,
    ResponseRoot,
    TradeQueryParams,
)

ResponseCls = TypeVar("ResponseCls", bound=ResponseRoot[Any])


class UJSONResponseHandler(BaseResponseHandler):
    """JSON response handler that uses ujson."""

    @staticmethod
    def get_request_data(response: APIClientResponse) -> Optional[JsonType]:
        """Attempt to decode the response data."""
        raw_data = response.get_raw_data()
        if raw_data == "":
            return None
        try:
            response_json = ujson.loads(raw_data)
        except ujson.JSONDecodeError as exc:
            msg = f"Unable to decode response data to json. data='{raw_data}'"
            raise ResponseParseError(msg) from exc
        return response_json


class CryptoWatchClient(APIClient):
    """The CryptoWatch client class."""

    def __init__(self, api_key: Optional[str] = None) -> None:
        api_key = api_key or settings.CW_API_KEY
        self._api_key = api_key
        if not api_key:
            authentication_method = NoAuthentication()
        else:
            authentication_method = HeaderAuthentication(
                token=api_key,
                parameter="X-CW-API-Key",
                scheme=None,
            )

        super().__init__(
            response_handler=UJSONResponseHandler,
            authentication_method=authentication_method,
        )

    @property
    def is_authenticated(self) -> bool:
        """Check whether an API has been provided."""
        return self._api_key is not None

    def get_info(self) -> ResponseRoot[Info]:
        """Get the allowance and status information by requesting root."""
        # NOTE: supposedly this returns the allowance, however, we get status info only
        return self._make_request(Endpoint.root, ResponseRoot[Info])

    def list_assets(
        self,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> PaginatedResponse[AssetList]:
        """List all available assets."""
        params = PaginationQueryParams(cursor=cursor, limit=limit)
        return self._make_request(
            Endpoint.list_assets,
            PaginatedResponse[AssetList],
            params=params,
        )

    def get_asset(self, asset_code: str) -> Response[Asset]:
        """Get information about a specific asset."""
        return self._make_request(
            Endpoint.asset_detail.format(assetCode=asset_code),
            Response[Asset],
        )

    def list_pairs(
        self,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> PaginatedResponse[PairList]:
        """List all available pairs."""
        params = PaginationQueryParams(cursor=cursor, limit=limit)
        return self._make_request(
            Endpoint.list_pairs,
            PaginatedResponse[PairList],
            params=params,
        )

    def get_pair(self, pair: str) -> Response[Pair]:
        """Get information about a specific pair."""
        return self._make_request(
            Endpoint.pair_detail.format(pair=pair),
            Response[Pair],
        )

    def list_markets(
        self,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> PaginatedResponse[MarketList]:
        """List all markets."""
        params = PaginationQueryParams(cursor=cursor, limit=limit)
        return self._make_request(
            Endpoint.list_markets,
            PaginatedResponse[MarketList],
            params=params,
        )

    def get_market(self, exchange: str, pair: str) -> Response[Market]:
        """Get information about a specific market."""
        return self._make_request(
            Endpoint.market_detail.format(exchange=exchange, pair=pair),
            Response[Market],
        )

    def get_market_price(self, exchange: str, pair: str) -> Response[MarketPrice]:
        """Get the last available price for a market."""
        return self._make_request(
            Endpoint.market_price.format(exchange=exchange, pair=pair),
            Response[MarketPrice],
        )

    def get_all_market_prices(
        self,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> PaginatedResponse[AllPrices]:
        """Get all market prices."""
        params = PaginationQueryParams(cursor=cursor, limit=limit)
        return self._make_request(
            Endpoint.all_market_prices,
            PaginatedResponse[AllPrices],
            params=params,
        )

    def get_market_trades(
        self,
        exchange: str,
        pair: str,
        since: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Response[MarketTradeList]:
        """Get recent trades for a market."""
        params = TradeQueryParams(since=since, limit=limit)
        return self._make_request(
            Endpoint.list_market_trades.format(exchange=exchange, pair=pair),
            Response[MarketTradeList],
            params=params,
        )

    def get_market_summary(
        self,
        exchange: str,
        pair: str,
    ) -> Response[MarketSummary]:
        """Get a 24h summary of a specific market.

        Returns a market's last price as well as other stats based on a
        24-hour sliding window.
        - High price
        - Low price
        - % change
        - Absolute change
        - Volume
        - Quote volume
        """
        return self._make_request(
            Endpoint.market_summary.format(exchange=exchange, pair=pair),
            Response[MarketSummary],
        )

    def get_all_market_summaries(
        self,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        key_by: Optional[str] = None,
    ) -> Response[AllSummaries]:
        """Get 24h summaries of all markets."""
        # TODO: use alias in unstructuring for params and in structuring for responses
        params = MarketSummariesQueryParams(
            cursor=cursor,
            limit=limit,
            key_by=key_by,
        )
        return self._make_request(
            Endpoint.all_market_summaries,
            Response[AllSummaries],
            params=params,
        )

    def get_market_order_book(  # noqa: PLR0913
        self,
        exchange: str,
        pair: str,
        depth: Optional[int] = None,
        span: Optional[float] = None,
        limit: Optional[int] = None,
    ) -> Response[OrderBook]:
        """Get the order book for a specific market."""
        params = OrderBookQueryParams(depth=depth, span=span, limit=limit)
        return self._make_request(
            Endpoint.market_orderbook.format(exchange=exchange, pair=pair),
            Response[OrderBook],
            params=params,
        )

    def get_market_order_book_liquidity(
        self,
        exchange: str,
        pair: str,
    ) -> Response[OrderBookLiquidity]:
        """Get liquidity sums at several basis point levels in the order book."""
        return self._make_request(
            Endpoint.market_orderbook_liquidity.format(exchange=exchange, pair=pair),
            Response[OrderBookLiquidity],
        )

    def calculate_quote(
        self,
        exchange: str,
        pair: str,
        amount: float,
    ) -> Response[OrderBookCalculator]:
        """Get a live quote from the order book for a given buy & sell amount."""
        params = OrderBookCalculatorQueryParams(amount=amount)
        return self._make_request(
            Endpoint.market_orderbook_calculator.format(exchange=exchange, pair=pair),
            Response[OrderBookCalculator],
            params=params,
        )

    def get_ohlcv(  # noqa: PLR0913
        self,
        exchange: str,
        pair: str,
        before: Optional[int] = None,
        after: Optional[int] = None,
        periods: Optional[List[Union[str, int]]] = None,
    ) -> Response[OHLCVDict]:
        """Get a market's OHLCV candlestick data."""
        params = OHLCVQueryParams(
            before=before,
            after=after,
            periods=periods,
        )
        return self._make_request(
            Endpoint.market_ohlc.format(exchange=exchange, pair=pair),
            Response[OHLCVDict],
            params=params,
        )

    def list_exchanges(self) -> Response[ExchangeList]:
        """List all exchanges."""
        return self._make_request(Endpoint.list_exchanges, Response[ExchangeList])

    def get_exchange(self, exchange: str) -> Response[Exchange]:
        """Get information about a specific exchange."""
        return self._make_request(
            Endpoint.exchange_detail.format(exchange=exchange),
            Response[Exchange],
        )

    def list_exchange_markets(self, exchange: str) -> Response[ExchangeMarkets]:
        """List all markets available on a given exchange."""
        return self._make_request(
            Endpoint.exchange_markets.format(exchange=exchange),
            Response[ExchangeMarkets],
        )

    def _make_request(
        self,
        endpoint: str,
        response_cls: Type[ResponseCls],
        params: Optional[attrs.AttrsInstance] = None,
    ) -> ResponseCls:
        """Make a request to the API."""
        params_dict = converter.unstructure(params) if params else None
        return self._structure_response(
            self.get(endpoint, params=params_dict),
            response_cls,
        )

    def _structure_response(
        self,
        response: JsonType,
        response_cls: Type[ResponseCls],
    ) -> ResponseCls:
        """Structure the response."""
        try:
            return converter.structure(
                response,
                response_cls,
            )
        except cattrs.errors.ClassValidationError as exc:
            msg = f"Failed to structure response: '{response}'"
            raise ResponseStructureError(msg) from exc
