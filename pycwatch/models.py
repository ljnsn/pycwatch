import enum
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Dict, Generic, List, Optional, TypeVar, Union

from pydantic import BaseModel, ConstrainedList, Extra, Field, HttpUrl, validator
from pydantic.generics import GenericModel

from pycwatch import utils

if TYPE_CHECKING:
    from pydantic.typing import CallableGenerator


def gen_alias(field_name: str) -> str:
    if field_name == "id_":
        return "id"
    return "".join(
        [w if i == 0 else w.capitalize() for i, w in enumerate(field_name.split("_"))]
    )


class Base(BaseModel):
    class Config:
        allow_population_by_field_name = True
        extra = Extra.forbid
        alias_generator = gen_alias


class CustomList(ConstrainedList):
    item_type: Any

    def __init_subclass__(cls) -> None:
        cls.__args__ = (cls.item_type,)

    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        for cls_validator in super().__get_validators__():
            yield cls_validator
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> "CustomList":
        return cls(v)


# query params


class PaginationQueryParams(Base):
    cursor: Optional[str] = None
    limit: Optional[int] = Field(None, le=5000)


class TradeQueryParams(Base):
    since: Optional[int]
    limit: Optional[int]


class MarketSummaryKey(str, enum.Enum):
    ID = "id"
    SYMBOLS = "symbols"


class MarketSummariesQueryParams(PaginationQueryParams):
    key_by: Optional[MarketSummaryKey] = Field(alias="keyBy")


class OrderBookQueryParams(Base):
    depth: Optional[int]
    span: Optional[float]
    limit: Optional[int]


class OrderBookCalculatorQueryParams(Base):
    # NOTE: this is float, not Decimal, because it will be sent
    amount: float


class OHLCVQueryParams(Base):
    before: Optional[int]
    after: Optional[int]
    periods: Optional[str]

    @validator("periods", pre=True)
    def list_to_str(cls, v: List[Union[str, int]]) -> Optional[str]:
        if not v:
            return None

        return utils.resolve_periods(v)


# path params


class AssetPathParams(Base):
    asset_code: str


class PairPathParams(Base):
    pair: str


class MarketPathParams(Base):
    exchange: str
    pair: str


class ExchangePathParams(Base):
    exchange: str


# models


ResultT = TypeVar("ResultT")


class Cursor(Base):
    last: str
    has_more: bool = Field(alias="hasMore")


class AllowanceBase(Base):
    cost: int
    remaining: int


class AllowanceAnonymous(AllowanceBase):
    upgrade: str


class AllowanceAuthenticated(AllowanceBase):
    remaining_paid: float = Field(alias="remainingPaid")
    account: str


Allowance = Union[AllowanceAnonymous, AllowanceAuthenticated]


class ResponseRoot(GenericModel, Generic[ResultT]):
    result: ResultT


class Response(ResponseRoot, Generic[ResultT]):
    allowance: Allowance


class PaginatedResponse(Response[ResultT], Generic[ResultT]):
    cursor: Cursor


class Route(HttpUrl):
    pass


class Info(Base):
    revision: str
    uptime: str
    documentation: Route
    indexes: List[Route]


class ListMember(Base):
    route: Route


class AssetBase(Base):
    id_: int
    symbol: str
    name: str
    fiat: bool
    sid: Optional[str]


class AssetMember(ListMember, AssetBase):
    pass


class AssetList(CustomList):
    item_type = AssetMember


class MarketBase(Base):
    id_: int
    exchange: str
    pair: str
    active: bool


class PairBase(Base):
    id_: int
    symbol: str
    base: AssetMember
    quote: AssetMember
    futuresContractPeriod: Optional[str] = None


class PairMember(ListMember, PairBase):
    pass


class PairList(CustomList):
    item_type = PairMember


class MarketMember(ListMember, MarketBase):
    pass


class AssetMarketList(Base):
    base: Optional[List[MarketMember]] = None
    quote: Optional[List[MarketMember]] = None


class Asset(AssetBase):
    markets: AssetMarketList


class MarketList(CustomList):
    item_type = MarketMember


class Pair(PairBase):
    route: Route
    markets: MarketList


class MarketRoutes(Base):
    price: Route
    summary: Route
    orderbook: Route
    trades: Route
    ohlc: Route


class Market(MarketBase):
    routes: MarketRoutes


class Price(Decimal):
    pass


class MarketPrice(Base):
    price: Price


AllPrices = Dict[str, Price]


class Trade(Base):
    id_: str
    timestamp: int
    price: Price
    amount: Decimal

    @classmethod
    def validate(cls, v: List[Any]) -> "Trade":
        return cls(
            id_=v[0],
            timestamp=v[1],
            price=v[2],
            amount=v[3],
        )


class MarketTradeList(CustomList):
    item_type = Trade


class PriceChange(Base):
    percentage: Decimal
    absolute: Decimal


class PriceSummary(Base):
    last: Decimal
    high: Decimal
    low: Decimal
    change: PriceChange


class MarketSummary(Base):
    price: PriceSummary
    volume: Decimal
    volume_quote: Decimal = Field(alias="volumeQuote")


AllSummaries = Dict[str, MarketSummary]


class OrderBookItem(Base):
    price: Price
    amount: Decimal

    @classmethod
    def validate(cls, v: List[Any]) -> "OrderBookItem":
        return cls(
            price=v[0],
            amount=v[1],
        )


class OrderBookArray(CustomList):
    item_type = OrderBookItem


class OrderBook(Base):
    asks: OrderBookArray
    bids: OrderBookArray
    seq_num: int = Field(alias="seqNum")


class LiquidityLevel(Base):
    base: Dict[int, Decimal]
    quote: Dict[int, Decimal]


class OrderBookLiquidity(Base):
    bid: LiquidityLevel
    ask: LiquidityLevel


class QuoteBase(Base):
    avg_price: Price
    avg_delta: Decimal
    avg_delta_bps: Decimal
    reach_price: Price
    reach_delta: Decimal
    reach_delta_bps: Decimal


class QuoteBuy(QuoteBase):
    spend: Decimal


class QuoteSell(QuoteBase):
    receive: Decimal


class OrderBookCalculator(Base):
    buy: QuoteBuy
    sell: QuoteSell


class OHLCV(Base):
    close_time: int
    open_price: Price
    high_price: Price
    low_price: Price
    close_price: Price
    volume: Decimal
    quote_volume: Decimal

    @classmethod
    def validate(cls, v: List[Any]) -> "OHLCV":
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


class ExchangeBase(Base):
    id_: int
    symbol: str
    name: str
    active: bool


class ExchangeMember(ListMember, ExchangeBase):
    pass


class ExchangeList(CustomList):
    item_type = ExchangeMember


class ExchangeRoutes(Base):
    markets: Route


class Exchange(ExchangeBase):
    routes: ExchangeRoutes


class ExchangeMarkets(CustomList):
    item_type = MarketMember
