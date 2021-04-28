"""Defines all API resources"""
from typing import Dict, List, Optional, Union


PERIOD_VALUES = {
    "1m": 60,
    "3m": 180,
    "5m": 300,
    "15m": 900,
    "30m": 1800,
    "1h": 3600,
    "2h": 7200,
    "4h": 14400,
    "6h": 21600,
    "12h": 43200,
    "1d": 86400,
    "3d": 259200,
    "1w": 604800,
}


class BaseResource:
    params: list = []

    @property
    def endpoint(self) -> str:
        return NotImplemented

    @property
    def query_parameters(self) -> Dict[str, str]:
        params = {}
        for param in self.params:
            if getattr(self, param):
                params[param] = getattr(self, param)
        return params


class ListAssetsResource(BaseResource):
    @property
    def endpoint(self) -> str:
        return "/assets"


class AssetDetailsResource(BaseResource):
    def __init__(self, asset_code: str) -> None:
        self.asset_code = asset_code

    @property
    def endpoint(self) -> str:
        return "/assets/{asset_code}".format(asset_code=self.asset_code)


class ListPairsResource(BaseResource):
    @property
    def endpoint(self) -> str:
        return "/pairs"


class PairDetailsResource(BaseResource):
    def __init__(self, pair: str) -> None:
        self.pair = pair

    @property
    def endpoint(self) -> str:
        return "/pairs/{pair}".format(pair=self.pair)


class ListMarketsResource(BaseResource):
    @property
    def endpoint(self) -> str:
        return "/markets"


class MarketDetailsResource(BaseResource):
    def __init__(self, exchange: str, pair: str) -> None:
        self.exchange = exchange
        self.pair = pair

    @property
    def endpoint(self) -> str:
        return "/markets/{exchange}/{pair}".format(
            exchange=self.exchange, pair=self.pair
        )


class MarketPriceResource(BaseResource):
    def __init__(self, exchange: str, pair: str) -> None:
        self.exchange = exchange
        self.pair = pair

    @property
    def endpoint(self) -> str:
        return "/markets/{exchange}/{pair}/price".format(
            exchange=self.exchange, pair=self.pair
        )


class AllMarketPricesResource(BaseResource):
    @property
    def endpoint(self) -> str:
        return "/markets/prices"


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

    params = ["since", "limit"]

    def __init__(
        self,
        exchange: str,
        pair: str,
        since: Optional[Union[int, str]] = None,
        limit: Optional[Union[int, str]] = None,
    ) -> None:
        self.exchange = exchange
        self.pair = pair
        self.since = since
        self.limit = limit

    @property
    def endpoint(self) -> str:
        return "/markets/{exchange}/{pair}/trades".format(
            exchange=self.exchange, pair=self.pair
        )


class MarketSummaryResource(BaseResource):
    def __init__(self, exchange: str, pair: str) -> None:
        self.exchange = exchange
        self.pair = pair

    @property
    def endpoint(self) -> str:
        return "/markets/{exchange}/{pair}/summary".format(
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

    params = ["keyBy"]

    def __init__(self, key_by: Optional[str] = None) -> None:
        self.keyBy = key_by

    @property
    def endpoint(self) -> str:
        return "/markets/summaries"


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

    params = ["depth", "span", "limit"]

    def __init__(
        self,
        exchange: str,
        pair: str,
        depth: Optional[Union[float, int, str]] = None,
        span: Optional[Union[float, int, str]] = None,
        limit: Optional[Union[int, str]] = None,
    ) -> None:
        self.exchange = exchange
        self.pair = pair
        self.depth = depth
        self.span = span
        self.limit = limit

    @property
    def endpoint(self) -> str:
        return "/markets/{exchange}/{pair}/orderbook".format(
            exchange=self.exchange, pair=self.pair
        )


class MarketOrderBookLiquidityResource(BaseResource):
    def __init__(self, exchange: str, pair: str) -> None:
        self.exchange = exchange
        self.pair = pair

    @property
    def endpoint(self) -> str:
        return "/markets/{exchange}/{pair}/orderbook/liquidity".format(
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

    params = ["before", "after", "periods"]

    def __init__(
        self,
        exchange: str,
        pair: str,
        before: Optional[Union[int, str]] = None,
        after: Optional[Union[int, str]] = None,
        periods: Optional[Union[List[Union[int, str]], str]] = None,
    ) -> None:
        self.exchange = exchange
        self.pair = pair
        self.before = before
        self.after = after

        if periods is not None:

            if not isinstance(periods, list):
                periods = [periods]

            parsed_periods = []
            for period in periods:
                if isinstance(period, str):
                    period = PERIOD_VALUES[period.lower()]
                parsed_periods.append(str(period))

            periods = ",".join(parsed_periods)

        self.periods = periods

    @property
    def endpoint(self) -> str:
        return "/markets/{exchange}/{pair}/ohlc".format(
            exchange=self.exchange, pair=self.pair
        )


class ListExchangesResource(BaseResource):
    @property
    def endpoint(self) -> str:
        return "/exchanges"


class ExchangeDetailsResource(BaseResource):
    def __init__(self, exchange) -> None:
        self.exchange = exchange

    @property
    def endpoint(self) -> str:
        return "/exchanges/{exchange}".format(exchange=self.exchange)


class ExchangeMarketsResource(BaseResource):
    def __init__(self, exchange) -> None:
        self.exchange = exchange

    @property
    def endpoint(self) -> str:
        return "/markets/{exchange}".format(exchange=self.exchange)


Resource = Union[
    AllMarketPricesResource,
    AllMarketSummariesResource,
    AssetDetailsResource,
    ExchangeDetailsResource,
    ExchangeMarketsResource,
    ListAssetsResource,
    ListExchangesResource,
    ListMarketsResource,
    ListPairsResource,
    MarketDetailsResource,
    MarketOHLCResource,
    MarketOrderBookLiquidityResource,
    MarketOrderBookResource,
    MarketPriceResource,
    MarketSummaryResource,
    MarketTradesResource,
    PairDetailsResource,
]
