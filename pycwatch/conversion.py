"""The converter for converting between Python objects and JSON."""

import sys
from decimal import Decimal
from typing import Any, Callable, Dict, List, Mapping, Type

if sys.version_info < (3, 8):
    from typing_extensions import Protocol
else:
    from typing import Protocol

import attrs
import cattrs
from cattrs.gen import make_dict_structure_fn, make_dict_unstructure_fn

converter = cattrs.Converter()


def _to_alias_unstructure(cls: Type[Any]) -> Callable[[Any], Dict[str, Any]]:
    """Unstructure hook using alias."""
    return make_dict_unstructure_fn(
        cls,
        converter,
        _cattrs_use_alias=True,
    )


def _to_alias_structure(
    cls: Type[Any],
) -> Callable[[Mapping[str, Any], Any], Callable[[Any, Any], Any]]:
    """Structure hook using alias."""
    return make_dict_structure_fn(
        cls,
        converter,
        _cattrs_use_alias=True,
    )


class IsList(Protocol):
    """Protocol for checking whether a value is a list."""

    @classmethod
    def from_list(cls, v: List[Any]) -> "IsList":
        """Create an instance from a list."""


def _structure_from_list(value: Any, type_: Type[IsList]) -> IsList:
    """Structure hook using from_list."""
    return type_.from_list(value)


converter.register_unstructure_hook_factory(attrs.has, _to_alias_unstructure)
converter.register_structure_hook_factory(attrs.has, _to_alias_structure)
converter.register_structure_hook(Decimal, lambda v, _: Decimal(str(v)))
converter.register_structure_hook_func(
    lambda t: hasattr(t, "from_list"),
    _structure_from_list,
)
