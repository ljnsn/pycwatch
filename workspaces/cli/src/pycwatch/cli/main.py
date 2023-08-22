"""Main CLI entrypoint."""

import typer

from pycwatch.cli.assets import app as assets_app
from pycwatch.cli.exchanges import app as exchanges_app
from pycwatch.cli.markets import app as markets_app
from pycwatch.cli.pairs import app as pairs_app
from pycwatch.cli.utils import FormatOption, OutputFormat, echo, get_client
from pycwatch.lib import CryptoWatchClient

app = typer.Typer(name="PyCwatch CLI")
app.add_typer(assets_app)
app.add_typer(pairs_app)
app.add_typer(markets_app)
app.add_typer(exchanges_app)


@app.command()
def info(ctx: typer.Context, style: FormatOption = OutputFormat.RECORDS) -> None:
    """Get API info."""
    response = get_client(ctx).get_info()
    echo(response.result, style)


@app.callback()
def main(ctx: typer.Context) -> None:
    """PyCwatch CLI."""
    ctx.meta["client"] = CryptoWatchClient()
