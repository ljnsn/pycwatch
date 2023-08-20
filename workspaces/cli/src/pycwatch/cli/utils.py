"""Utils for CLI."""

from typing import cast

import typer

from pycwatch.lib import CryptoWatchClient


def get_client(ctx: typer.Context) -> CryptoWatchClient:
    """Get client from context."""
    return cast(CryptoWatchClient, ctx.meta["client"])
