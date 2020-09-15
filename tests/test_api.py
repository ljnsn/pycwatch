
import pytest

import pycwatch


def test_list_assets():
    api = pycwatch.rest
    assets = api.list_assets()
