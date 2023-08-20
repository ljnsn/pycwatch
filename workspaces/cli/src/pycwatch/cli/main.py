"""Main CLI entrypoint."""

import typer
from rich import print

from pycwatch.cli.assets import app as assets_app
from pycwatch.cli.pairs import app as pairs_app
from pycwatch.cli.utils import get_client
from pycwatch.lib import CryptoWatchClient
from pycwatch.lib.conversion import converter

app = typer.Typer(name="PyCwatch CLI")
app.add_typer(assets_app)
app.add_typer(pairs_app)


@app.command()
def info(ctx: typer.Context) -> None:
    """Get API info."""
    result = get_client(ctx).get_info()
    print(converter.unstructure(result))


@app.callback()
def main(ctx: typer.Context) -> None:
    """PyCwatch CLI."""
    ctx.meta["client"] = CryptoWatchClient()
