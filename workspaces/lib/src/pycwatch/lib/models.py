"""All models used by the package."""

import enum
from decimal import Decimal
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

import attrs

from pycwatch.lib import utils

# query params


@attrs.define()
class PaginationQueryParams:
    """Query parameters used for paginated calls."""

    cursor: Optional[str] = None
    limit: Optional[int] = attrs.field(
        default=None,
        validator=attrs.validators.optional(
            [
                attrs.validators.instance_of(int),
                attrs.validators.le(5000),
            ]
        ),
    )


@attrs.define()
class TradeQueryParams:
    """Query parameters for trades."""

    since: Optional[int] = attrs.field(
        validator=attrs.validators.optional(attrs.validators.instance_of(int))
    )
    limit: Optional[int] = attrs.field(
        validator=attrs.validators.optional(attrs.validators.instance_of(int))
    )


class MarketSummaryKey(str, enum.Enum):
    """Keys for market summary calls."""

    ID = "id"
    SYMBOLS = "symbols"


@attrs.define()
class MarketSummariesQueryParams(PaginationQueryParams):
    """Query parameters for market summary calls."""

    key_by: Optional[MarketSummaryKey] = attrs.field(
        default=None,
        converter=attrs.converters.optional(MarketSummaryKey),
        validator=attrs.validators.optional(
            attrs.validators.instance_of(MarketSummaryKey)
        ),
    )


@attrs.define()
class OrderBookQueryParams:
    """Query parameters for order book calls."""

    depth: Optional[int] = attrs.field(
        validator=attrs.validators.optional(attrs.validators.instance_of(int))
    )
    span: Optional[float] = attrs.field(
        validator=attrs.validators.optional(attrs.validators.instance_of(float))
    )
    limit: Optional[int] = attrs.field(
        validator=attrs.validators.optional(attrs.validators.instance_of(int))
    )


@attrs.define()
class OrderBookCalculatorQueryParams:
    """Query parameters for order book calculator calls."""

    # NOTE: this is float, not Decimal, because it will be sent
    amount: Union[float, int] = attrs.field(
        validator=attrs.validators.instance_of((float, int))
    )


@attrs.define()
class OHLCVQueryParams:  # type: ignore[no-untyped-def]
    """Query parameters for OHLCV calls."""

    before: Optional[int] = attrs.field(
        default=None,
        validator=attrs.validators.optional(attrs.validators.instance_of(int)),
    )
    after: Optional[int] = attrs.field(
        default=None,
        validator=attrs.validators.optional(attrs.validators.instance_of(int)),
    )
    periods: Optional[str] = attrs.field(  # type: ignore[var-annotated]
        default=None,
        converter=attrs.converters.optional(
            lambda value: None if not value else utils.resolve_periods(value)
        ),
        validator=attrs.validators.optional(attrs.validators.instance_of(str)),
    )


# path params


@attrs.define()
class AssetPathParams:
    """Path parameters for asset calls."""

    asset_code: str = attrs.field(validator=attrs.validators.instance_of(str))


@attrs.define()
class PairPathParams:
    """Path parameters for pair calls."""

    pair: str = attrs.field(validator=attrs.validators.instance_of(str))


@attrs.define()
class MarketPathParams:
    """Path parameters for market calls."""

    exchange: str = attrs.field(validator=attrs.validators.instance_of(str))
    pair: str = attrs.field(validator=attrs.validators.instance_of(str))


@attrs.define()
class ExchangePathParams:
    """Path parameters for exchange calls."""

    exchange: str = attrs.field(validator=attrs.validators.instance_of(str))


# models


ResultT = TypeVar("ResultT")


@attrs.define()
class Cursor:
    """A cursor used for pagination."""

    last: str
    has_more: bool


@attrs.define()
class AllowanceBase:
    """Base class for allowance models."""

    cost: int
    remaining: int


@attrs.define()
class AllowanceAnonymous(AllowanceBase):
    """Allowance model for anonymous calls."""

    upgrade: str


@attrs.define()
class AllowanceAuthenticated(AllowanceBase):
    """Allowance model for authenticated calls."""

    remaining_paid: float
    account: str


Allowance = Union[AllowanceAnonymous, AllowanceAuthenticated]


@attrs.define()
class ResponseRoot(Generic[ResultT]):
    """Root response class."""

    result: ResultT


@attrs.define()
class Response(ResponseRoot[ResultT], Generic[ResultT]):
    """Response class."""

    allowance: Allowance


@attrs.define()
class PaginatedResponse(Response[ResultT], Generic[ResultT]):
    """Paginated response class."""

    cursor: Cursor


Route = str


@attrs.define()
class Info:
    """Info model."""

    revision: str
    uptime: str
    documentation: Route
    indexes: List[Route]


@attrs.define()
class ListMember:
    """Base class for list members."""

    route: Route


@attrs.define()
class AssetBase:
    """Base class for asset models."""

    id_: int
    symbol: str
    name: str
    fiat: bool
    sid: Optional[str]


@attrs.define()
class AssetMember(AssetBase):
    """A member of an asset list."""

    route: Route


AssetList = List[AssetMember]


@attrs.define()
class MarketBase:
    """Base class for market models."""

    id_: int
    exchange: str
    pair: str
    active: bool


@attrs.define(kw_only=True)
class PairBase:
    """Base class for pair models."""

    id_: int
    symbol: str
    base: AssetMember
    quote: AssetMember
    futures_contract_period: Optional[str] = None


@attrs.define(kw_only=True)
class PairMember(PairBase):
    """A member of a pair list."""

    route: Route


PairList = List[PairMember]


@attrs.define()
class MarketMember(MarketBase):
    """A member of a market list."""

    route: Route


MarketList = List[MarketMember]


@attrs.define()
class AssetMarketList:
    """A list of markets for an asset."""

    base: Optional[MarketList] = None
    quote: Optional[MarketList] = None


@attrs.define()
class Asset(AssetBase):
    """Asset model."""

    markets: AssetMarketList


@attrs.define(kw_only=True)
class Pair(PairBase):
    """Pair model."""

    route: Route
    markets: MarketList


@attrs.define()
class MarketRoutes:
    """Routes for a market."""

    price: Route
    summary: Route
    orderbook: Route
    trades: Route
    ohlc: Route


@attrs.define()
class Market(MarketBase):
    """Market model."""

    routes: MarketRoutes


Price = Decimal


@attrs.define()
class MarketPrice:
    """Market price model."""

    price: Price


AllPrices = Dict[str, Price]


@attrs.define()
class Trade:
    """Trade model."""

    id_: str
    timestamp: int
    price: Price
    amount: Decimal

    @classmethod
    def from_list(cls, v: List[Any]) -> "Trade":
        """Create a Trade from a list."""
        return cls(
            id_=v[0],
            timestamp=v[1],
            price=v[2],
            amount=v[3],
        )


MarketTradeList = List[Trade]


@attrs.define()
class PriceChange:
    """Price change model."""

    percentage: Decimal
    absolute: Decimal


@attrs.define()
class PriceSummary:
    """Price summary model."""

    last: Decimal
    high: Decimal
    low: Decimal
    change: PriceChange


@attrs.define()
class MarketSummary:
    """Market summary model."""

    price: PriceSummary
    volume: Decimal
    volume_quote: Decimal


AllSummaries = Dict[str, MarketSummary]


@attrs.define()
class OrderBookItem:
    """Order book item model."""

    price: Price
    amount: Decimal

    @classmethod
    def from_list(cls, v: List[Any]) -> "OrderBookItem":
        """Create an OrderBookItem from a list."""
        return cls(
            price=v[0],
            amount=v[1],
        )


OrderBookArray = List[OrderBookItem]


@attrs.define()
class OrderBook:
    """Order book model."""

    asks: OrderBookArray
    bids: OrderBookArray
    seq_num: int


@attrs.define()
class LiquidityLevel:
    """Liquidity level model."""

    base: Dict[int, Decimal]
    quote: Dict[int, Decimal]


@attrs.define()
class OrderBookLiquidity:
    """Order book liquidity model."""

    bid: LiquidityLevel
    ask: LiquidityLevel


@attrs.define()
class QuoteBase:
    """Base class for quote models."""

    avg_price: Price
    avg_delta: Decimal
    avg_delta_bps: Decimal
    reach_price: Price
    reach_delta: Decimal
    reach_delta_bps: Decimal


@attrs.define()
class QuoteBuy(QuoteBase):
    """Buy quote model."""

    spend: Decimal


@attrs.define()
class QuoteSell(QuoteBase):
    """Sell quote model."""

    receive: Decimal


@attrs.define()
class OrderBookCalculator:
    """Order book calculator model."""

    buy: QuoteBuy
    sell: QuoteSell


@attrs.define()
class OHLCV:
    """OHLCV model."""

    close_time: int
    open_price: Price
    high_price: Price
    low_price: Price
    close_price: Price
    volume: Decimal
    quote_volume: Decimal

    @classmethod
    def from_list(cls, v: List[Any]) -> "OHLCV":
        """Create an OHLCV from a list."""
        return cls(
            close_time=v[0],
            open_price=v[1],
            high_price=v[2],
            low_price=v[3],
            close_price=v[4],
            volume=v[5],
            quote_volume=v[6],
        )


OHLCVDict = Dict[str, List[OHLCV]]


@attrs.define()
class ExchangeBase:
    """Base class for exchange models."""

    id_: int
    symbol: str
    name: str
    active: bool


@attrs.define()
class ExchangeMember(ExchangeBase):
    """A member of an exchange list."""

    route: Route


ExchangeList = List[ExchangeMember]


@attrs.define()
class ExchangeRoutes:
    """Routes for an exchange."""

    markets: Route


@attrs.define()
class Exchange(ExchangeBase):
    """Exchange model."""

    routes: ExchangeRoutes


ExchangeMarkets = List[MarketMember]
