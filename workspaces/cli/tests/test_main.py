from typer.testing import CliRunner

from pycwatch.cli.main import app


def test_info(runner: CliRunner) -> None:
    """Verify that the info command works."""
    result = runner.invoke(app, ["info"])
    assert result.exit_code == 0
