import pytest

from pycwatch.models import OHLCVQueryParams


def test_ohlcv_list_to_str():
    periods = [60, 180, 300]
    lstring = OHLCVQueryParams.list_to_str(periods)
    assert lstring == "60,180,300"
    assert OHLCVQueryParams.list_to_str([]) is None

    with pytest.raises(TypeError, match="all periods must be integers"):
        OHLCVQueryParams.list_to_str(["60", "180", "300"])
