from typing import Optional

from apiclient import APIClient
from apiclient.authentication_methods import HeaderAuthentication, NoAuthentication
from apiclient.response_handlers import JsonResponseHandler
from apiclient_pydantic import serialize_all_methods

from .config import settings
from .endpoints import Endpoint
from .models import (
    AllPrices,
    AllSummaries,
    Asset,
    AssetList,
    AssetPathParams,
    Exchange,
    ExchangeList,
    ExchangeMarkets,
    ExchangePathParams,
    Info,
    Market,
    MarketList,
    MarketPathParams,
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
    PairPathParams,
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


@serialize_all_methods()
class CryptoWatchClient(APIClient):
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

    def get_info(self) -> ResponseRoot[Info]:
        """Get the allowance and status information by requesting root."""
        # NOTE: supposedly this returns the allowance, however, we get status info only
        return self.get(Endpoint.root)

    def list_assets(
        self, params: PaginationQueryParams
    ) -> PaginatedResponse[AssetList]:
        """List all available assets."""
        return self.get(Endpoint.list_assets, params=params)

    def get_asset(self, path_params: AssetPathParams) -> Response[Asset]:
        """Get information about a specific asset."""
        return self.get(Endpoint.asset_detail.format(**path_params))

    def list_pairs(self, params: PaginationQueryParams) -> PaginatedResponse[PairList]:
        """List all available pairs."""
        return self.get(Endpoint.list_pairs, params=params)

    def get_pair(self, path_params: PairPathParams) -> Response[Pair]:
        """Get information about a specific pair."""
        return self.get(Endpoint.pair_detail.format(**path_params))

    def list_markets(
        self, params: PaginationQueryParams
    ) -> PaginatedResponse[MarketList]:
        """List all markets."""
        return self.get(Endpoint.list_markets, params=params)

    def get_market(self, path_params: MarketPathParams) -> Response[Market]:
        """Get information about a specific market."""
        return self.get(Endpoint.market_detail.format(**path_params))

    def get_market_price(self, path_params: MarketPathParams) -> Response[MarketPrice]:
        """Get the last available price for a market."""
        return self.get(Endpoint.market_price.format(**path_params))

    def get_all_market_prices(
        self, params: PaginationQueryParams
    ) -> PaginatedResponse[AllPrices]:
        """Get all market prices."""
        return self.get(Endpoint.all_market_prices, params=params)

    def get_market_trades(
        self, path_params: MarketPathParams, params: TradeQueryParams
    ) -> Response[MarketTradeList]:
        """Get recent trades for a market."""
        return self.get(
            Endpoint.list_market_trades.format(**path_params), params=params
        )

    def get_market_summary(
        self, path_params: MarketPathParams
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
        return self.get(Endpoint.market_summary.format(**path_params))

    def get_all_market_summaries(
        self, params: MarketSummariesQueryParams
    ) -> Response[AllSummaries]:
        """Get 24h summaries of all markets."""
        return self.get(Endpoint.all_market_summaries, params=params)

    def get_market_order_book(
        self, path_params: MarketPathParams, params: OrderBookQueryParams
    ) -> Response[OrderBook]:
        """Get the order book for a specific market."""
        return self.get(Endpoint.market_orderbook.format(**path_params), params=params)

    def get_market_order_book_liquidity(
        self, path_params: MarketPathParams
    ) -> Response[OrderBookLiquidity]:
        """Get liquidity sums at several basis point levels in the order book."""
        return self.get(Endpoint.market_orderbook_liquidity.format(**path_params))

    def calculate_quote(
        self, path_params: MarketPathParams, params: OrderBookCalculatorQueryParams
    ) -> Response[OrderBookCalculator]:
        """Get a live quote from the order book for a given buy & sell amount."""
        return self.get(
            Endpoint.market_orderbook_calculator.format(**path_params), params=params
        )

    def get_ohlcv(
        self, path_params: MarketPathParams, params: OHLCVQueryParams
    ) -> Response[OHLCVDict]:
        """Get a market's OHLCV candlestick data."""
        return self.get(Endpoint.market_ohlc.format(**path_params), params=params)

    def list_exchanges(self) -> Response[ExchangeList]:
        """List all exchanges."""
        return self.get(Endpoint.list_exchanges)

    def get_exchange(self, path_params: ExchangePathParams) -> Response[Exchange]:
        """Get information about a specific exchange."""
        return self.get(Endpoint.exchange_detail.format(**path_params))

    def list_exchange_markets(
        self, path_params: ExchangePathParams
    ) -> Response[ExchangeMarkets]:
        """List all markets available on a given exchange."""
        return self.get(Endpoint.exchange_markets.format(**path_params))
