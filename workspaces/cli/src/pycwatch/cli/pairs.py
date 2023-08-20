"""Commands related to pairs."""

from typing import Annotated, Optional

import typer
from rich import print

from pycwatch.cli.utils import get_client
from pycwatch.lib.conversion import converter

# ruff: noqa: B008

app = typer.Typer(name="pairs", help="Get or list pairs.")


@app.command(name="list")
def list_pairs(
    ctx: typer.Context,
    cursor: Annotated[Optional[str], typer.Option()] = None,  # noqa: UP007
    limit: Annotated[Optional[int], typer.Option()] = None,  # noqa: UP007
) -> None:
    """List pairs."""
    result = get_client(ctx).list_pairs(cursor, limit)
    print(converter.unstructure(result))


@app.command(name="get")
def get_pair(
    ctx: typer.Context,
    code: str = typer.Argument(..., help="Pair identifier."),
) -> None:
    """Get pair."""
    result = get_client(ctx).get_pair(code)
    print(converter.unstructure(result))
