from functools import reduce

import pytest

from pycwatch.rest import HTTPClient, BaseResource


def log_has(line, logs):
    # caplog mocker returns log as a tuple: `(module, level, message)`
    # and we want to match line against `message` in the tuple
    return reduce(
        lambda a, b: a or b,
        filter(lambda x: x[2] == line, logs.record_tuples),
        False
    )


@pytest.fixture
def api_key():
    return 'abcdefghijklmnopqrstuvwxyz'


@pytest.fixture
def http_client():
    client = HTTPClient(None, None)
    return client


class MockResource(BaseResource):
    params = ['param']

    def __init__(self, part, param):
        self.part = part
        self.param = param

    @property
    def endpoint(self):
        return '/path/{part}'.format(part=self.part)


@pytest.fixture
def mock_resource():
    resource = MockResource('test-part', 'test-value')
    return resource


def register_resource(mocker, resource, method, status_code, json=None,
                      text=None):
    mocker.register_uri(method, resource, status_code=status_code, json=json,
                        text=text)
