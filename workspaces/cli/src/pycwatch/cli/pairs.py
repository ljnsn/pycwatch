"""Commands related to pairs."""

import typer

from pycwatch.cli.utils import (
    CursorOption,
    FormatOption,
    LimitOption,
    OutputFormat,
    echo,
    get_client,
)

app = typer.Typer(name="pairs", help="Get or list pairs.")


@app.command(name="list")
def list_pairs(
    ctx: typer.Context,
    cursor: CursorOption = None,
    limit: LimitOption = None,
    style: FormatOption = OutputFormat.RECORDS,
) -> None:
    """List pairs."""
    response = get_client(ctx).list_pairs(cursor, limit)
    echo(response.result, style)


@app.command(name="get")
def get_pair(
    ctx: typer.Context,
    code: str = typer.Argument(..., help="Pair identifier."),
    style: FormatOption = OutputFormat.RECORDS,
) -> None:
    """Get pair."""
    response = get_client(ctx).get_pair(code)
    echo(response.result, style)
