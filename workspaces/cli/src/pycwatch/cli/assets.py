"""Commands related to assets."""

from typing import Annotated, Optional

import typer
from rich import print

from pycwatch.cli.utils import get_client
from pycwatch.lib.conversion import converter

app = typer.Typer(name="assets", help="Get or list assets.")


@app.command(name="list")
def list_assets(
    ctx: typer.Context,
    cursor: Annotated[Optional[str], typer.Option()] = None,
    limit: Annotated[Optional[int], typer.Option()] = None,
) -> None:
    """List assets."""
    response = get_client(ctx).list_assets(cursor, limit)
    print(converter.unstructure(response.result))


@app.command(name="get")
def get_asset(
    ctx: typer.Context,
    code: str = typer.Argument(..., help="Asset code."),
) -> None:
    """Get asset."""
    response = get_client(ctx).get_asset(code)
    print(converter.unstructure(response.result))
