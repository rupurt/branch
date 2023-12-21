import time
from datetime import datetime
from pathlib import Path
from typing_extensions import Annotated
import typer
from pydantic import ValidationError
from result import Ok, Err
from rich import print
from rich.text import Text
from branch.config import default_config, read_settings
from branch.core import adapter, create_topic, Topic
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
def create(
    name: Annotated[
        str,
        typer.Option(
            help="topic name",
        ),
    ],
    partitions: Annotated[
        int,
        typer.Option(
            help="number of topic partitions, min=1, max=200_000",
        ),
    ],
    storage_location: Annotated[
        str,
        typer.Option(
            help="persistent storage uri, e.g. local://.branch, gcp://my-bucket?token=gcp_credentials.json",
        ),
    ],
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose",
            "-v",
            help="display information about the created topic",
        ),
    ] = False,
    config: Path = typer.Option(
        default_config,
        callback=conf_callback,
        is_eager=True,
        help="path to config file",
    ),
):
    start_at = time.perf_counter()
    adapter_result = adapter(storage_location)
    if isinstance(adapter_result, Err):
        print(Text(f"{adapter_result.err()}", style="red"))
        raise typer.Exit(2)
    create_result = create_topic(
        name=name, partitions=partitions, storage=adapter_result.ok()
    )
    if isinstance(create_result, Err):
        __print_create_error__(create_result)
        raise typer.Exit(2)
    end_at = time.perf_counter()
    run_time = end_at - start_at
    if verbose:
        __print_verbose__(create_result, run_time)


def __print_create_error__(create_result):
    err = create_result.err()
    if isinstance(err, ValidationError):
        for validation in ValidationError.errors(err):
            msg = validation["msg"].lower()
            for attr in validation["loc"]:
                print(Text(f"{attr} {msg}", style="red"))
    else:
        print(Text(err, style="red"))


def __print_verbose__(create_result: Ok[Topic], run_time: float):
    topic = create_result.ok()
    run_time_fmt = Text.assemble(
        Text(f"{run_time:0.6f}", style="bright_cyan"), " seconds"
    )
    items = [
        ("name", topic.name),
        ("partitions", topic.partitions),
        ("retention", float("inf")),
        ("created_at", topic.created_at),
        ("updated_at", topic.updated_at),
        ("time", run_time_fmt),
    ]
    print(Text("successfully created topic", style="green"))
    __print_items__(items)


def __print_items__(items):
    for key, value in items:
        content = None
        if isinstance(value, str):
            content = Text.assemble(f"- {key}=", Text(f'"{value}"', style="yellow"))
        elif isinstance(value, datetime):
            content = Text.assemble(f"- {key}=", Text(f"{value}", style="bright_cyan"))
        elif isinstance(value, Text):
            content = Text.assemble(f"- {key}=", value)
        elif isinstance(value, int):
            content = Text.assemble(f"- {key}=", Text(f"{value}", style="bright_cyan"))
        elif value == float("inf"):
            content = Text.assemble(
                f"- {key}=", Text("infinite", style="bright_magenta")
            )
        print(content)
