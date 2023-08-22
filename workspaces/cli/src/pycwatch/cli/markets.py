"""Commands related to markets."""

from typing import Annotated, Optional

import typer

from pycwatch.cli.utils import (
    CursorOption,
    FormatOption,
    LimitOption,
    OutputFormat,
    echo,
    get_client,
)
from pycwatch.lib.models import MarketSummaryKey

app = typer.Typer(name="markets", help="Get or list markets.")


@app.command(name="list")
def list_markets(
    ctx: typer.Context,
    cursor: CursorOption = None,
    limit: LimitOption = None,
    style: FormatOption = OutputFormat.RECORDS,
) -> None:
    """List markets."""
    response = get_client(ctx).list_markets(cursor, limit)
    echo(response.result, style)


@app.command(name="get")
def get_market(
    ctx: typer.Context,
    exchange: str,
    pair: str,
    style: FormatOption = OutputFormat.RECORDS,
) -> None:
    """Get a market."""
    response = get_client(ctx).get_market(exchange, pair)
    echo(response.result, style)


@app.command(name="price")
def get_market_price(
    ctx: typer.Context,
    exchange: str,
    pair: str,
    style: FormatOption = OutputFormat.RECORDS,
) -> None:
    """Get a market price."""
    response = get_client(ctx).get_market_price(exchange, pair)
    echo(response.result, style)


@app.command(name="prices")
def list_market_prices(
    ctx: typer.Context,
    cursor: CursorOption = None,
    limit: LimitOption = None,
    style: FormatOption = OutputFormat.RECORDS,
) -> None:
    """Get a market price."""
    response = get_client(ctx).get_all_market_prices(cursor, limit)
    echo(response.result, style)


@app.command(name="trades")
def get_market_trades(  # noqa: PLR0913
    ctx: typer.Context,
    exchange: str,
    pair: str,
    since: Annotated[Optional[int], typer.Option()] = None,
    limit: LimitOption = None,
    style: FormatOption = OutputFormat.RECORDS,
) -> None:
    """Get market trades."""
    response = get_client(ctx).get_market_trades(exchange, pair, since, limit)
    echo(response.result, style)


@app.command(name="summary")
def get_market_summary(
    ctx: typer.Context,
    exchange: str,
    pair: str,
    style: FormatOption = OutputFormat.RECORDS,
) -> None:
    """Get a market summary."""
    response = get_client(ctx).get_market_summary(exchange, pair)
    echo(response.result, style)


@app.command(name="summaries")
def list_market_summaries(
    ctx: typer.Context,
    cursor: CursorOption = None,
    limit: LimitOption = None,
    key_by: Annotated[Optional[MarketSummaryKey], typer.Option()] = None,
    style: FormatOption = OutputFormat.RECORDS,
) -> None:
    """List market summaries."""
    key = None if key_by is None else MarketSummaryKey(key_by)
    response = get_client(ctx).get_all_market_summaries(cursor, limit, key)
    echo(response.result, style)


@app.command(name="orderbook")
def get_market_orderbook(  # noqa: PLR0913
    ctx: typer.Context,
    exchange: str,
    pair: str,
    depth: Annotated[Optional[int], typer.Option("--depth", "-d")] = None,
    span: Annotated[Optional[int], typer.Option("--span", "-s")] = None,
    limit: LimitOption = None,
    style: FormatOption = OutputFormat.RECORDS,
) -> None:
    """Get a market's order book."""
    response = get_client(ctx).get_market_order_book(exchange, pair, depth, span, limit)
    echo(response.result, style)


@app.command(name="orderbook-liquidity")
def get_market_order_book_liquidity(
    ctx: typer.Context,
    exchange: str,
    pair: str,
    style: FormatOption = OutputFormat.RECORDS,
) -> None:
    """Get a market's order book liquidity."""
    response = get_client(ctx).get_market_order_book_liquidity(exchange, pair)
    echo(response.result, style)


@app.command(name="calculate")
def calculate_quote(
    ctx: typer.Context,
    exchange: str,
    pair: str,
    amount: float,
    style: FormatOption = OutputFormat.RECORDS,
) -> None:
    """Get a live quote from the order book for a given buy & sell amount."""
    response = get_client(ctx).calculate_quote(exchange, pair, amount)
    echo(response.result, style)


@app.command(name="ohlcv")
def get_market_ohlcv(  # noqa: PLR0913
    ctx: typer.Context,
    exchange: str,
    pair: str,
    before: Annotated[Optional[int], typer.Option("-b", "--before")] = None,
    after: Annotated[Optional[int], typer.Option("-a", "--after")] = None,
    periods: Annotated[Optional[list[str]], typer.Option("-p", "--periods")] = None,
    style: FormatOption = OutputFormat.RECORDS,
) -> None:
    """Get a market's OHLCV data."""
    periods_ = (
        periods
        if periods is None
        else [int(period) if period.isdigit() else period for period in periods]
    )
    response = get_client(ctx).get_ohlcv(
        exchange,
        pair,
        before,
        after,
        periods_,  # type: ignore[arg-type]
    )
    echo(response.result, style)
