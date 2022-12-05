"""The module that holds the API client."""
from typing import List, Optional, Union

from apiclient import APIClient
from apiclient.authentication_methods import HeaderAuthentication, NoAuthentication
from apiclient.response_handlers import JsonResponseHandler
from apiclient_pydantic import serialize_response

from .config import settings
from .endpoints import Endpoint
from .models import (
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

NO_KEY_MESSAGE = """\
You have not set an API Key. Anonymous users are limited to 10 Cryptowatch
Credits worth of API calls per 24-hour period.

See https://docs.cryptowat.ch/rest-api/rate-limit#api-request-pricing-structure
for more information.\
"""


class CryptoWatchClient(APIClient):
    """The CryptoWatch client class."""

    def __init__(self, api_key: Optional[str] = None) -> None:
        api_key = api_key or settings.CW_API_KEY
        self._api_key = api_key
        if not api_key:
            print(NO_KEY_MESSAGE)
            authentication_method = NoAuthentication()
        else:
            authentication_method = HeaderAuthentication(
                token=api_key, parameter="X-CW-API-Key", scheme=None
            )

        super().__init__(
            response_handler=JsonResponseHandler,
            authentication_method=authentication_method,
        )

    @property
    def is_authenticated(self) -> bool:
        """Check whether an API has been provided."""
        return self._api_key is not None

    @serialize_response()
    def get_info(self) -> ResponseRoot[Info]:
        """Get the allowance and status information by requesting root."""
        # NOTE: supposedly this returns the allowance, however, we get status info only
        return self.get(Endpoint.root)

    @serialize_response()
    def list_assets(
        self,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> PaginatedResponse[AssetList]:
        """List all available assets."""
        params = PaginationQueryParams(cursor=cursor, limit=limit)
        return self.get(Endpoint.list_assets, params=params.dict())

    @serialize_response()
    def get_asset(self, asset_code: str) -> Response[Asset]:
        """Get information about a specific asset."""
        return self.get(Endpoint.asset_detail.format(assetCode=asset_code))

    @serialize_response()
    def list_pairs(
        self,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> PaginatedResponse[PairList]:
        """List all available pairs."""
        params = PaginationQueryParams(cursor=cursor, limit=limit)
        return self.get(Endpoint.list_pairs, params=params.dict())

    @serialize_response()
    def get_pair(self, pair: str) -> Response[Pair]:
        """Get information about a specific pair."""
        return self.get(Endpoint.pair_detail.format(pair=pair))

    @serialize_response()
    def list_markets(
        self,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> PaginatedResponse[MarketList]:
        """List all markets."""
        params = PaginationQueryParams(cursor=cursor, limit=limit)
        return self.get(Endpoint.list_markets, params=params.dict())

    @serialize_response()
    def get_market(self, exchange: str, pair: str) -> Response[Market]:
        """Get information about a specific market."""
        return self.get(Endpoint.market_detail.format(exchange=exchange, pair=pair))

    @serialize_response()
    def get_market_price(self, exchange: str, pair: str) -> Response[MarketPrice]:
        """Get the last available price for a market."""
        return self.get(Endpoint.market_price.format(exchange=exchange, pair=pair))

    @serialize_response()
    def get_all_market_prices(
        self,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> PaginatedResponse[AllPrices]:
        """Get all market prices."""
        params = PaginationQueryParams(cursor=cursor, limit=limit)
        return self.get(Endpoint.all_market_prices, params=params.dict())

    @serialize_response()
    def get_market_trades(
        self,
        exchange: str,
        pair: str,
        since: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Response[MarketTradeList]:
        """Get recent trades for a market."""
        params = TradeQueryParams(since=since, limit=limit)
        return self.get(
            Endpoint.list_market_trades.format(exchange=exchange, pair=pair),
            params=params.dict(),
        )

    @serialize_response()
    def get_market_summary(
        self,
        exchange: str,
        pair: str,
    ) -> Response[MarketSummary]:
        """Get a 24h summary of a specific market.

        Returns a market's last price as well as other stats based on a 24-hour sliding window.
        - High price
        - Low price
        - % change
        - Absolute change
        - Volume
        - Quote volume
        """
        return self.get(Endpoint.market_summary.format(exchange=exchange, pair=pair))

    @serialize_response()
    def get_all_market_summaries(
        self,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        key_by: Optional[str] = None,
    ) -> Response[AllSummaries]:
        """Get 24h summaries of all markets."""
        params = MarketSummariesQueryParams(
            cursor=cursor,
            limit=limit,
            key_by=key_by,  # type: ignore
        )
        return self.get(Endpoint.all_market_summaries, params=params.dict())

    @serialize_response()
    def get_market_order_book(
        self,
        exchange: str,
        pair: str,
        depth: Optional[int] = None,
        span: Optional[float] = None,
        limit: Optional[int] = None,
    ) -> Response[OrderBook]:
        """Get the order book for a specific market."""
        params = OrderBookQueryParams(depth=depth, span=span, limit=limit)
        return self.get(
            Endpoint.market_orderbook.format(exchange=exchange, pair=pair),
            params=params.dict(),
        )

    @serialize_response()
    def get_market_order_book_liquidity(
        self,
        exchange: str,
        pair: str,
    ) -> Response[OrderBookLiquidity]:
        """Get liquidity sums at several basis point levels in the order book."""
        return self.get(
            Endpoint.market_orderbook_liquidity.format(exchange=exchange, pair=pair)
        )

    @serialize_response()
    def calculate_quote(
        self,
        exchange: str,
        pair: str,
        amount: float,
    ) -> Response[OrderBookCalculator]:
        """Get a live quote from the order book for a given buy & sell amount."""
        params = OrderBookCalculatorQueryParams(amount=amount)
        return self.get(
            Endpoint.market_orderbook_calculator.format(exchange=exchange, pair=pair),
            params=params.dict(),
        )

    @serialize_response()
    def get_ohlcv(
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
            periods=periods,  # type: ignore
        )
        return self.get(
            Endpoint.market_ohlc.format(exchange=exchange, pair=pair),
            params=params.dict(),
        )

    @serialize_response()
    def list_exchanges(self) -> Response[ExchangeList]:
        """List all exchanges."""
        return self.get(Endpoint.list_exchanges)

    @serialize_response()
    def get_exchange(self, exchange: str) -> Response[Exchange]:
        """Get information about a specific exchange."""
        return self.get(Endpoint.exchange_detail.format(exchange=exchange))

    @serialize_response()
    def list_exchange_markets(self, exchange: str) -> Response[ExchangeMarkets]:
        """List all markets available on a given exchange."""
        return self.get(Endpoint.exchange_markets.format(exchange=exchange))
