from apiclient import APIClient
from apiclient.response_handlers import JsonResponseHandler
from apiclient_pydantic import serialize_all_methods

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
    TradeQueryParams,
)


@serialize_all_methods()
class CryptoWatchClient(APIClient):
    def __init__(self) -> None:
        super().__init__(response_handler=JsonResponseHandler)

    def list_assets(
        self, params: PaginationQueryParams
    ) -> PaginatedResponse[AssetList]:
        return self.get(Endpoint.list_assets, params=params)

    def get_asset(self, path_params: AssetPathParams) -> Response[Asset]:
        return self.get(Endpoint.asset_detail.format(**path_params))

    def list_pairs(self, params: PaginationQueryParams) -> PaginatedResponse[PairList]:
        return self.get(Endpoint.list_pairs, params=params)

    def get_pair(self, path_params: PairPathParams) -> Response[Pair]:
        return self.get(Endpoint.pair_detail.format(**path_params))

    def list_markets(
        self, params: PaginationQueryParams
    ) -> PaginatedResponse[MarketList]:
        return self.get(Endpoint.list_markets, params=params)

    def get_market(self, path_params: MarketPathParams) -> Response[Market]:
        return self.get(Endpoint.market_detail.format(**path_params))

    def get_market_price(self, path_params: MarketPathParams) -> Response[MarketPrice]:
        return self.get(Endpoint.market_price.format(**path_params))

    def get_all_market_prices(
        self, params: PaginationQueryParams
    ) -> PaginatedResponse[AllPrices]:
        return self.get(Endpoint.all_market_prices, params=params)

    def get_market_trades(
        self, path_params: MarketPathParams, params: TradeQueryParams
    ) -> Response[MarketTradeList]:
        return self.get(
            Endpoint.list_market_trades.format(**path_params), params=params
        )

    def get_market_summary(
        self, path_params: MarketPathParams
    ) -> Response[MarketSummary]:
        return self.get(Endpoint.market_summary.format(**path_params))

    def get_all_market_summaries(
        self, params: MarketSummariesQueryParams
    ) -> Response[AllSummaries]:
        return self.get(Endpoint.all_market_summaries, params=params)

    def get_market_order_book(
        self, path_params: MarketPathParams, params: OrderBookQueryParams
    ) -> Response[OrderBook]:
        return self.get(Endpoint.market_orderbook.format(**path_params), params=params)

    def get_market_order_book_liquidity(
        self, path_params: MarketPathParams
    ) -> Response[OrderBookLiquidity]:
        return self.get(Endpoint.market_orderbook_liquidity.format(**path_params))

    def calculate_quote(
        self, path_params: MarketPathParams, params: OrderBookCalculatorQueryParams
    ) -> Response[OrderBookCalculator]:
        return self.get(
            Endpoint.market_orderbook_calculator.format(**path_params), params=params
        )

    def get_ohlcv(
        self, path_params: MarketPathParams, params: OHLCVQueryParams
    ) -> Response[OHLCVDict]:
        return self.get(Endpoint.market_ohlc.format(**path_params), params=params)

    def list_exchanges(self) -> Response[ExchangeList]:
        return self.get(Endpoint.list_exchanges)

    def get_exchange(self, path_params: ExchangePathParams) -> Response[Exchange]:
        return self.get(Endpoint.exchange_detail.format(**path_params))

    def list_exchange_markets(
        self, path_params: ExchangePathParams
    ) -> Response[ExchangeMarkets]:
        return self.get(Endpoint.exchange_markets.format(**path_params))
