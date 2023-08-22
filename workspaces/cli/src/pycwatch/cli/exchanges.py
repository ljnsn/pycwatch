"""Commands related to exchanges."""

import typer

from pycwatch.cli.utils import FormatOption, OutputFormat, echo, get_client

app = typer.Typer(name="exchanges", help="Get or list exchanges.")


@app.command(name="list")
def list_exchanges(
    ctx: typer.Context,
    style: FormatOption = OutputFormat.RECORDS,
) -> None:
    """List exchanges."""
    response = get_client(ctx).list_exchanges()
    echo(response.result, style)


@app.command(name="get")
def get_exchange(
    ctx: typer.Context,
    code: str = typer.Argument(..., help="Exchange code."),
    style: FormatOption = OutputFormat.RECORDS,
) -> None:
    """Get exchange."""
    response = get_client(ctx).get_exchange(code)
    echo(response.result, style)


@app.command(name="markets")
def list_exchange_markets(
    ctx: typer.Context,
    code: str = typer.Argument(..., help="Exchange code."),
    style: FormatOption = OutputFormat.RECORDS,
) -> None:
    """List exchange markets."""
    response = get_client(ctx).list_exchange_markets(code)
    echo(response.result, style)
