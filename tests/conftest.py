"""Fixtures and configuration for the test suite."""
from pathlib import Path

import pytest
import vcr

from pycwatch import CryptoWatchClient


BASE_DIR = Path(__file__).parent.absolute()

api_vcr = my_vcr = vcr.VCR(
    serializer="yaml",
    cassette_library_dir=BASE_DIR.joinpath("vcr_cassettes").as_posix(),
    record_mode="new_episodes",
    match_on=["uri", "method", "query"],
    decode_compressed_response=True,
)


@pytest.fixture()
def live_client():
    return CryptoWatchClient()


@pytest.fixture
def api_key():
    return "abcdefghijklmnopqrstuvwxyz"
