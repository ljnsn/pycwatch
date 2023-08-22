"""Utils for CLI."""

import csv
import enum
import io
from collections.abc import Mapping, Sequence
from typing import Annotated, Any, Optional, cast

import attrs
import typer
from rich.console import Console
from rich.table import Table

from pycwatch.lib import CryptoWatchClient
from pycwatch.lib.conversion import converter


class OutputFormat(str, enum.Enum):
    """Output format."""

    RECORDS = "records"
    OBJECTS = "objects"
    JSON = "json"
    CSV = "csv"
    TABLE = "table"


FormatOption = Annotated[
    OutputFormat,
    typer.Option("-f", "--format", help="The output format"),
]
LimitOption = Annotated[
    Optional[int],
    typer.Option("-l", "--limit", help="Maximum number of items to include"),
]
CursorOption = Annotated[
    Optional[str],
    typer.Option("-c", "--cursor", help="Cursor for pagination"),
]


def get_client(ctx: typer.Context) -> CryptoWatchClient:
    """Get client from context."""
    return cast(CryptoWatchClient, ctx.meta["client"])


def echo(
    output: attrs.AttrsInstance | Sequence[attrs.AttrsInstance] | Mapping[str, Any],
    style: FormatOption,
) -> None:
    """Write output to stdout."""
    console = Console()
    match style:
        case OutputFormat.RECORDS:
            unstructured_data = converter.unstructure(output)
            print_maybe_paged(console, unstructured_data)
        case OutputFormat.OBJECTS:
            print_maybe_paged(console, output)
        case OutputFormat.JSON:
            console.print_json(converter.dumps(output))
        case OutputFormat.CSV:
            unstructured_data = converter.unstructure(output)
            if isinstance(output, dict):
                unstructured_data = add_top_level_as_key(unstructured_data)
            console.print(write_csv(unstructured_data).read())
        case OutputFormat.TABLE:
            unstructured_data = converter.unstructure(output)
            if isinstance(output, dict):
                unstructured_data = add_top_level_as_key(unstructured_data)
            console.print(write_table(unstructured_data))


def add_top_level_as_key(data: dict[str, Any]) -> list[dict[str, Any]]:
    """Add the top level as a key."""
    output = []
    for key, value in data.items():
        if isinstance(value, dict):
            output.append({"key": key, **value})
        elif isinstance(value, list):
            for item in value:
                output.append({"key": key, **item})
        else:
            output.append({"key": key, "value": value})
    return output


def print_maybe_paged(console: Console, data: Any, threshold: int = 20) -> None:
    """Write output to stdout, paging if necessary."""
    if isinstance(data, list) and len(data) > threshold:
        with console.pager():
            console.print(data)
    else:
        console.print(data)


def write_table(data: dict[str, Any] | list[dict[str, Any]]) -> Table:
    """Write output to a table."""
    table = Table()
    headers = data.keys() if isinstance(data, dict) else data[0].keys()
    for header in headers:
        table.add_column(header)
    if isinstance(data, dict):
        table.add_row(*dict_to_row(data))
    else:
        for item in data:
            table.add_row(*dict_to_row(item))
    return table


def dict_to_row(data: dict[str, Any]) -> list[Any]:
    """Write a dict to a table row."""
    row: list[Any] = []
    for value in data.values():
        if isinstance(value, dict):
            row.append(write_table(value))
        elif isinstance(value, list):
            row.append(", ".join([str(v) for v in value]))
        else:
            row.append(str(value))
    return row


def write_csv(data: dict[str, Any] | list[dict[str, Any]]) -> io.StringIO:
    """Write output to an in-memory buffer as CSV."""
    output = io.StringIO()
    if isinstance(data, dict):
        flattened_data = flatten_dict(data)
        writer = csv.DictWriter(output, fieldnames=flattened_data.keys())
        writer.writeheader()
        writer.writerow(flattened_data)
    else:
        flattened_list = [flatten_dict(d) for d in data]
        writer = csv.DictWriter(output, fieldnames=flattened_list[0].keys())
        writer.writeheader()
        for record in flattened_list:
            writer.writerow(record)
    output.seek(0)
    return output


def flatten_dict(
    dictionary: dict[str, Any],
    parent_key: str = "",
    sep: str = "_",
) -> dict[str, Any]:
    """Flatten a nested dictionary structure."""
    flattened_dict = {}
    for key, value in dictionary.items():
        new_key = parent_key + sep + key if parent_key else key
        if isinstance(value, dict):
            flattened_dict.update(flatten_dict(value, new_key, sep))
        else:
            flattened_dict[new_key] = value
    return flattened_dict
