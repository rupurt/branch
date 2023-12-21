from pathlib import Path
import typer
from result import Err
from typing_extensions import Annotated
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
def consume(
    topic: Annotated[
        str,
        typer.Option(
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
    print("TODO... topics consume")
    print(storage_location)
    print(topic)

    adapter_result = branch.core.adapter(storage_location)
    if isinstance(adapter_result, Err):
        print(adapter_result.err())
        raise typer.Exit(2)

    # def consume_record(record):
    #     print("received new record")
    #     print(record)
    #
    # branch.consume(topic, consume_record)
