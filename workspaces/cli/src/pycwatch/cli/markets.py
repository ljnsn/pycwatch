"""Commands related to markets."""

from typing import Annotated, Optional

import typer
from rich import print

from pycwatch.cli.utils import get_client
from pycwatch.lib.conversion import converter

# ruff: noqa: B008

app = typer.Typer(name="markets", help="Get or list markets.")


@app.command(name="list")
def list_markets(
    ctx: typer.Context,
    cursor: Annotated[Optional[str], typer.Option()] = None,  # noqa: UP007
    limit: Annotated[Optional[int], typer.Option()] = None,  # noqa: UP007
) -> None:
    """List markets."""
    result = get_client(ctx).list_markets(cursor, limit)
    print(converter.unstructure(result))


@app.command(name="get")
def get_market(ctx: typer.Context, exchange: str, pair: str) -> None:
    """Get a market."""
    result = get_client(ctx).get_market(exchange, pair)
    print(converter.unstructure(result))


@app.command(name="price")
def get_market_price(ctx: typer.Context, exchange: str, pair: str) -> None:
    """Get a market price."""
    result = get_client(ctx).get_market_price(exchange, pair)
    print(converter.unstructure(result))


@app.command(name="prices")
def list_market_prices(
    ctx: typer.Context,
    cursor: Annotated[Optional[str], typer.Option()] = None,  # noqa: UP007
    limit: Annotated[Optional[int], typer.Option()] = None,  # noqa: UP007
) -> None:
    """Get a market price."""
    result = get_client(ctx).get_all_market_prices(cursor, limit)
    print(converter.unstructure(result))


@app.command(name="trades")
def get_market_trades(
    ctx: typer.Context,
    exchange: str,
    pair: str,
    since: Annotated[Optional[int], typer.Option()] = None,  # noqa: UP007
    limit: Annotated[Optional[int], typer.Option()] = None,  # noqa: UP007
) -> None:
    """Get market trades."""
    result = get_client(ctx).get_market_trades(exchange, pair, since, limit)
    print(converter.unstructure(result))


@app.command(name="summary")
def get_market_summary(ctx: typer.Context, exchange: str, pair: str) -> None:
    """Get a market summary."""
    response = get_client(ctx).get_market_summary(exchange, pair)
    print(converter.unstructure(response.result))


@app.command(name="summaries")
def list_market_summaries(
    ctx: typer.Context,
    cursor: Annotated[Optional[str], typer.Option()] = None,  # noqa: UP007
    limit: Annotated[Optional[int], typer.Option()] = None,  # noqa: UP007
    key_by: Annotated[Optional[str], typer.Option()] = None,  # noqa: UP007
) -> None:
    """List market summaries."""
    response = get_client(ctx).get_all_market_summaries(cursor, limit, key_by)
    print(converter.unstructure(response.result))


@app.command(name="orderbook")
def get_market_orderbook(  # noqa: PLR0913
    ctx: typer.Context,
    exchange: str,
    pair: str,
    depth: Annotated[
        Optional[int], typer.Option("--depth", "-d")  # noqa: UP007
    ] = None,
    span: Annotated[Optional[int], typer.Option("--span", "-s")] = None,  # noqa: UP007
    limit: Annotated[
        Optional[int], typer.Option("--limit", "-l")  # noqa: UP007
    ] = None,
) -> None:
    """Get a market's order book."""
    response = get_client(ctx).get_market_order_book(exchange, pair, depth, span, limit)
    print(converter.unstructure(response.result))


@app.command(name="orderbook-liquidity")
def get_market_order_book_liquidity(
    ctx: typer.Context,
    exchange: str,
    pair: str,
) -> None:
    """Get a market's order book liquidity."""
    response = get_client(ctx).get_market_order_book_liquidity(exchange, pair)
    print(converter.unstructure(response.result))


@app.command(name="calculate")
def calculate_quote(
    ctx: typer.Context,
    exchange: str,
    pair: str,
    amount: float,
) -> None:
    """Get a live quote from the order book for a given buy & sell amount."""
    response = get_client(ctx).calculate_quote(exchange, pair, amount)
    print(converter.unstructure(response.result))


@app.command(name="ohlcv")
def get_market_ohlcv(  # noqa: PLR0913
    ctx: typer.Context,
    exchange: str,
    pair: str,
    before: Annotated[
        Optional[int], typer.Option("-b", "--before")  # noqa: UP007
    ] = None,
    after: Annotated[
        Optional[int], typer.Option("-a", "--after")  # noqa: UP007
    ] = None,
    periods: Annotated[
        Optional[list[int | str]], typer.Option("-p", "--periods")  # noqa: UP007
    ] = None,
) -> None:
    """Get a market's OHLCV data."""
    response = get_client(ctx).get_ohlcv(exchange, pair, before, after, periods)
    print(converter.unstructure(response.result))
