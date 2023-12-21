from pathlib import Path
from typing import Optional
from typing_extensions import Annotated
from result import Ok, Err
import typer
from branch.config import default_config, read_settings
from branch.core import adapter, delete_topic
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
def delete(
    topic: Annotated[
        str,
        typer.Argument(
            help="topic name",
        ),
    ],
    storage_location: Annotated[
        str,
        typer.Option(
            help="persistent storage uri, e.g. local://.branch, gcp://my-bucket?token=gcp_credentials.json",
        ),
    ],
    verbose: Annotated[
        Optional[bool],
        typer.Option(
            "--verbose",
            "-v",
            help="display information about the deleted topic",
        ),
    ] = False,
    config: Path = typer.Option(
        default_config,
        callback=conf_callback,
        is_eager=True,
        help="path to config file",
    ),
):
    adapter_result = adapter(storage_location)
    if isinstance(adapter_result, Err):
        print(adapter_result.err())
        raise typer.Exit(2)
    delete_result = delete_topic(topic=topic, storage=adapter_result.ok())
    if isinstance(delete_result, Err):
        # __print_create_error__(create_result)
        raise typer.Exit(2)
    if verbose:
        __print_verbose__(delete_result)


def __print_verbose__(delete_result: Ok[None]):
    # topic = create_result.ok()
    # print("successfully created topic")
    # print(f"name={topic.name}")
    # print(f"partitions={topic.partitions}")
    # print(f"created_at={topic.created_at}")
    # print(f"updated_at={topic.updated_at}")
    print("TODO... delete topic")
