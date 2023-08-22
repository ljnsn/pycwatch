from typing import Any

import pytest

from pycwatch.cli import utils


@pytest.mark.parametrize(
    ("dict_in", "expected"),
    [
        (
            {"a": 1, "b": 2, "c": 3},
            [
                {"key": "a", "value": 1},
                {"key": "b", "value": 2},
                {"key": "c", "value": 3},
            ],
        ),
        (
            {"a": {"aa": 1, "ab": 2}, "b": {"ba": 3, "bb": 4}},
            [
                {"key": "a", "aa": 1, "ab": 2},
                {"key": "b", "ba": 3, "bb": 4},
            ],
        ),
        (
            {
                "a": [{"aa": 1, "ab": 2}, {"aa": 3, "ab": 4}],
                "b": [{"ba": 5, "bb": 6}],
            },
            [
                {"key": "a", "aa": 1, "ab": 2},
                {"key": "a", "aa": 3, "ab": 4},
                {"key": "b", "ba": 5, "bb": 6},
            ],
        ),
    ],
)
def test_top_level_as_dict(
    dict_in: dict[str, Any],
    expected: list[dict[str, Any]],
) -> None:
    """Verify that the top level is added as a key."""
    assert utils.add_top_level_as_key(dict_in) == expected
