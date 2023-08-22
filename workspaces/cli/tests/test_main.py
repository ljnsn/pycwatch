import pytest
from typer.testing import CliRunner

from pycwatch.cli.main import app


@pytest.mark.parametrize("style", ["records", "objects", "json", "csv", "table"])
def test_info(runner: CliRunner, style: str) -> None:
    """Verify that the info command works."""
    result = runner.invoke(app, ["info", "-f", style])
    assert result.exit_code == 0
