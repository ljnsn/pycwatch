from typer.testing import CliRunner

from pycwatch.cli.main import app


def test_list_markets(runner: CliRunner) -> None:
    """Verify that the list command works."""
    result = runner.invoke(app, ["markets", "list", "--limit", "10"])
    assert result.exit_code == 0


def test_get_market(runner: CliRunner) -> None:
    """Verify that the get command works."""
    result = runner.invoke(app, ["markets", "get", "kraken", "btceur"])
    assert result.exit_code == 0


def test_get_market_price(runner: CliRunner) -> None:
    """Verify that the get price command works."""
    result = runner.invoke(app, ["markets", "price", "kraken", "btceur"])
    assert result.exit_code == 0


def test_list_market_prices(runner: CliRunner) -> None:
    """Verify that the list prices command works."""
    result = runner.invoke(app, ["markets", "prices", "--limit", "10"])
    assert result.exit_code == 0


def test_get_market_trades(runner: CliRunner) -> None:
    """Verify that the get trades command works."""
    result = runner.invoke(app, ["markets", "trades", "kraken", "btceur"])
    assert result.exit_code == 0


def test_get_market_summary(runner: CliRunner) -> None:
    """Verify that the get summary command works."""
    result = runner.invoke(app, ["markets", "summary", "kraken", "btceur"])
    assert result.exit_code == 0


def test_list_market_summaries(runner: CliRunner) -> None:
    """Verify that the list summaries command works."""
    result = runner.invoke(app, ["markets", "summaries", "--limit", "10"])
    assert result.exit_code == 0


def test_get_market_orderbook(runner: CliRunner) -> None:
    """Verify that the get orderbook command works."""
    result = runner.invoke(app, ["markets", "orderbook", "kraken", "btceur"])
    assert result.exit_code == 0


def test_get_market_orderbook_liquidity(runner: CliRunner) -> None:
    """Verify that the get orderbook liquidity command works."""
    result = runner.invoke(
        app,
        ["markets", "orderbook-liquidity", "kraken", "btceur"],
    )
    assert result.exit_code == 0


def test_calculate_quote(runner: CliRunner) -> None:
    """Verify that the calculate command works."""
    result = runner.invoke(
        app,
        ["markets", "calculate", "kraken", "btceur", "2.0"],
    )
    assert result.exit_code == 0


def test_get_market_ohlcv(runner: CliRunner) -> None:
    """Verify that the get ohlcv command works."""
    result = runner.invoke(
        app,
        ["markets", "ohlcv", "kraken", "btceur", "-p", "1h"],
    )
    assert result.exit_code == 0
