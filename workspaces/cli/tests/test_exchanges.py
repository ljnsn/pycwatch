from typer.testing import CliRunner

from pycwatch.cli.main import app


def test_list_exchanges(runner: CliRunner) -> None:
    """Verify that the list command works."""
    result = runner.invoke(app, ["exchanges", "list"])
    assert result.exit_code == 0


def test_get_exchange(runner: CliRunner) -> None:
    """Verify that the get command works."""
    result = runner.invoke(app, ["exchanges", "get", "binance"])
    assert result.exit_code == 0


def test_list_exchange_markets(runner: CliRunner) -> None:
    """Verify that the list markets command works."""
    result = runner.invoke(app, ["exchanges", "markets", "binance"])
    assert result.exit_code == 0
