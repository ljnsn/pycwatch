"""The converter for converting between Python objects and JSON."""

import sys
from decimal import Decimal
from typing import Any, Callable, Dict, List, Mapping, Type

if sys.version_info < (3, 8):
    from typing_extensions import Protocol
else:
    from typing import Protocol

import attrs
from cattrs.gen import make_dict_structure_fn, make_dict_unstructure_fn, override
from cattrs.preconf.ujson import make_converter

converter = make_converter()


def to_cwatch_key(field_name: str) -> str:
    """
    Generate the fieldname understood by cryptowatch.

    Args:
        field_name: The python name of the field.

    Returns:
        The cryptowatch name.
    """
    if field_name == "id_":
        return "id"
    return "".join(
        [w if i == 0 else w.capitalize() for i, w in enumerate(field_name.split("_"))]
    )


def _to_alias_unstructure(cls: Type[Any]) -> Callable[[Any], Dict[str, Any]]:
    """Unstructure hook using alias."""
    return make_dict_unstructure_fn(
        cls,
        converter,
        **{a.name: override(rename=to_cwatch_key(a.name)) for a in attrs.fields(cls)},
    )


def _to_alias_structure(
    cls: Type[Any],
) -> Callable[[Mapping[str, Any], Any], Callable[[Any, Any], Any]]:
    """Structure hook using alias."""
    return make_dict_structure_fn(
        cls,
        converter,
        **{a.name: override(rename=to_cwatch_key(a.name)) for a in attrs.fields(cls)},
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
converter.register_unstructure_hook(Decimal, lambda v: str(v))
converter.register_structure_hook_func(
    lambda t: hasattr(t, "from_list"),
    _structure_from_list,
)
