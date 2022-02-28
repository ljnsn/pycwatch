"""Fixtures and configuration for the test suite."""
from functools import reduce
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


def log_has(line, logs):
    # caplog mocker returns log as a tuple: `(module, level, message)`
    # and we want to match line against `message` in the tuple
    return reduce(
        lambda a, b: a or b, filter(lambda x: line in x[2], logs.record_tuples), False
    )


@pytest.fixture()
def live_client():
    return CryptoWatchClient()


@pytest.fixture
def api_key():
    return "abcdefghijklmnopqrstuvwxyz"
