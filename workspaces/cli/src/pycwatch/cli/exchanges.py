"""Commands related to exchanges."""

import typer
from rich import print

from pycwatch.cli.utils import get_client
from pycwatch.lib.conversion import converter

# ruff: noqa: B008

app = typer.Typer(name="exchanges", help="Get or list exchanges.")


@app.command(name="list")
def list_exchanges(ctx: typer.Context) -> None:
    """List exchanges."""
    response = get_client(ctx).list_exchanges()
    print(converter.unstructure(response.result))


@app.command(name="get")
def get_exchange(
    ctx: typer.Context,
    code: str = typer.Argument(..., help="Exchange code."),
) -> None:
    """Get exchange."""
    response = get_client(ctx).get_exchange(code)
    print(converter.unstructure(response.result))


@app.command(name="markets")
def list_exchange_markets(
    ctx: typer.Context,
    code: str = typer.Argument(..., help="Exchange code."),
) -> None:
    """List exchange markets."""
    response = get_client(ctx).list_exchange_markets(code)
    print(converter.unstructure(response.result))
