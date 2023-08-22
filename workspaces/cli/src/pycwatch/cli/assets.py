"""Commands related to assets."""

import typer

from pycwatch.cli.utils import (
    CursorOption,
    FormatOption,
    LimitOption,
    OutputFormat,
    echo,
    get_client,
)

app = typer.Typer(name="assets", help="Get or list assets.")


@app.command(name="list")
def list_assets(
    ctx: typer.Context,
    cursor: CursorOption = None,
    limit: LimitOption = None,
    style: FormatOption = OutputFormat.RECORDS,
) -> None:
    """List assets."""
    response = get_client(ctx).list_assets(cursor, limit)
    echo(response.result, style)


@app.command(name="get")
def get_asset(
    ctx: typer.Context,
    code: str = typer.Argument(..., help="Asset code."),
    style: FormatOption = OutputFormat.RECORDS,
) -> None:
    """Get asset."""
    response = get_client(ctx).get_asset(code)
    echo(response.result, style)
