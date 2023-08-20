from typing import Optional

import pytest

from pycwatch.config import Settings


@pytest.mark.parametrize(
    ("env_key", "init_key", "expected"),
    [
        (None, None, None),
        (None, "bar", "bar"),
        ("foo", None, "foo"),
        ("foo", "bar", "bar"),
    ],
)
def test_settings(
    env_key: Optional[str],
    init_key: Optional[str],
    expected: Optional[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verify that settings are loaded correctly."""
    if env_key is not None:
        monkeypatch.setenv("CW_API_KEY", env_key)
    settings = Settings(init_key)

    assert expected == settings.CW_API_KEY
