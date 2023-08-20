from typing import Any, Dict

import attrs
import pytest

from pycwatch.conversion import converter


@attrs.define()
class FakeObject:
    """Object for testing."""

    id_: int
    foo_bar: str


@pytest.fixture(name="test_data")
def test_data_fixture() -> Dict[str, Any]:
    """Provide some test data."""
    return {"id": 1, "fooBar": "baz"}


@pytest.fixture(name="test_object")
def test_object_fixture() -> FakeObject:
    """Provide a test object."""
    return FakeObject(id_=1, foo_bar="baz")


def test_structuring(test_data: Dict[str, Any]) -> None:
    """Verify keys are structured to snake-case fields."""
    obj = converter.structure(test_data, FakeObject)

    assert obj.id_ == 1
    assert obj.foo_bar == "baz"


def test_unstructuring(test_object: FakeObject) -> None:
    """Verify fields are unstructured to camel-case keys."""
    data = converter.unstructure(test_object)

    assert data["id"] == 1
    assert data["fooBar"] == "baz"
