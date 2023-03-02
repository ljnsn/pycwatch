from typing import List, Optional, Union

import pytest
from pycwatch.models import OHLCVQueryParams


@pytest.mark.parametrize(
    ("periods", "expected"),
    [
        ([], None),
        ([60, 180, 300], "60,180,300"),
        ([60, 180, 604800, "604800_Monday"], "60,180,604800,604800_Monday"),
        (["1m", "30m", "1w_monday"], "60,1800,604800_Monday"),
        ([60, "30m"], "60,1800"),
        (["3m", 180], "180"),
    ],
)
def test_ohlcv_query_params(
    periods: List[Union[str, int]],
    expected: Optional[str],
) -> None:
    params = OHLCVQueryParams(periods=periods)

    assert params.periods == expected

    with pytest.raises(ValueError, match="Invalid period label"):
        OHLCVQueryParams(periods=["60", "180", "300"])
