"""Test config for CLI tests."""

import pytest
from typer.testing import CliRunner


@pytest.fixture(scope="session")
def runner() -> CliRunner:
    """Provide a CLI Runner."""
    return CliRunner()
