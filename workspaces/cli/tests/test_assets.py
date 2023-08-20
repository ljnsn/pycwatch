from typer.testing import CliRunner

from pycwatch.cli.main import app


def test_list_assets(runner: CliRunner) -> None:
    """Verify that the list command works."""
    result = runner.invoke(app, ["assets", "list", "--limit", "10"])
    assert result.exit_code == 0


def test_get_asset(runner: CliRunner) -> None:
    """Verify that the get command works."""
    result = runner.invoke(app, ["assets", "get", "iota"])
    assert result.exit_code == 0
