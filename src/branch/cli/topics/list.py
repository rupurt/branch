import typer
from typing_extensions import Annotated
from pathlib import Path
from rich.console import Console
from rich.table import Table
from result import Err
from branch.config import default_config, read_settings
import branch.core
from .main import app


def conf_callback(ctx: typer.Context, param: typer.CallbackParam, value: str):
    ctx.default_map = ctx.default_map or {}
    if value:
        try:
            settings = read_settings(value)
            default_map = {
                "storage_location": settings.storage.location,
            }
            ctx.default_map.update(default_map)
        except Exception:
            pass
    return value


@app.command()
def list(
    pattern: Annotated[
        str,
        typer.Argument(
            help="topic name filter, supports wildcard '*'",
        ),
    ],
    storage_location: Annotated[
        str,
        typer.Option(
            help="persistent storage uri, e.g. local://.branch, gcp://my-bucket?token=gcp_credentials.json",
        ),
    ],
    config: Path = typer.Option(
        default_config,
        callback=conf_callback,
        is_eager=True,
        help="path to config file",
    ),
):
    adapter_result = branch.core.adapter(storage_location)
    if isinstance(adapter_result, Err):
        print(adapter_result.err())
        raise typer.Exit(2)
    list_result = branch.core.glob_topics(pattern, storage=adapter_result.ok())
    if isinstance(list_result, Err):
        print(list_result.err())
        raise typer.Exit(2)
    table = Table(
        "Name",
        "Partitions",
        "Retention",
        "Created At",
        "Updated At",
    )
    for t in list_result.ok():
        table.add_row(
            t.name,
            str(t.partitions),
            __fmt_retention__(t.retention),
            str(t.created_at),
            str(t.updated_at),
        )
    console = Console()
    console.print(table)


def __fmt_retention__(retention):
    if retention is None:
        return "-"
    if retention.bytes is not None and retention.ms is not None:
        return f"bytes={retention.bytes}, ms={retention.ms}"
    elif retention.bytes is not None:
        return f"bytes={retention.bytes}"
    elif retention.ms is not None:
        return f"ms={retention.ms}"
