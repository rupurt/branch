from pathlib import Path
from typing_extensions import Annotated, Optional
import typer
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
def produce(
    topic: Annotated[
        str,
        typer.Option(
            help="topic name",
        ),
    ],
    partition: Annotated[
        int,
        typer.Option(
            help="topic partition",
        ),
    ],
    message: Annotated[
        str,
        typer.Option(
            help="value of a record that will assigned the next offset",
        ),
    ],
    storage_location: Annotated[
        str,
        typer.Option(
            help="persistent storage uri, e.g. local://.branch, gcp://my-bucket?token=gcp_credentials.json",
        ),
    ],
    key: Annotated[
        Optional[str],
        typer.Option(
            help="unique identifier for the record",
        ),
    ] = None,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose",
            "-v",
            help="display information about the produced record",
        ),
    ] = False,
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
    headers = {}
    producer_record = branch.core.ProducerRecord(
        topic=topic,
        partition=partition,
        key=key,
        headers=headers,
        value=message.encode(),
    )
    produce_result = branch.produce(
        record=producer_record,
        storage=adapter_result.ok(),
    )
    if isinstance(produce_result, Err):
        print(produce_result.err())
        typer.Exit(2)
    if verbose:
        print("TODO... print verbose stuff")
