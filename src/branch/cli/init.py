from pathlib import Path
import typer
from typing_extensions import Annotated, Optional
import yaml
from branch.config import (
    default_config,
    read_settings,
    Settings,
    ServerSettings,
    StorageSettings,
    CLISettings,
    CLITableSettings,
)
from branch.main import app


def conf_callback(ctx: typer.Context, param: typer.CallbackParam, value: str):
    ctx.default_map = ctx.default_map or {}
    if value:
        try:
            settings = read_settings(value)
            default_map = {
                "server_host": settings.server.host,
                "server_port": settings.server.port,
                "server_log_level": settings.server.log_level,
                "storage_location": settings.storage.location,
                "storage_create": settings.storage.create,
                "cli_table_width": settings.cli.table.width,
            }
            ctx.default_map.update(default_map)
        except Exception:
            pass
    return value


def server_host_prompt(default):
    return typer.prompt("server host", default=default)


def server_port_prompt(default):
    return typer.prompt("server port", default=default)


def server_log_level_prompt(default):
    return typer.prompt("server log level", default=default)


def storage_location_prompt(default):
    return typer.prompt("storage location", default=default)


def storage_create_prompt(default):
    return typer.prompt("storage create", default=default)


@app.command()
def init(
    storage_location: Annotated[
        str,
        typer.Option(
            callback=storage_location_prompt,
            help="storage engine persistence location",
        ),
    ],
    storage_create: Annotated[
        bool,
        typer.Option(
            callback=storage_create_prompt,
            help="todo...",
        ),
    ],
    server_host: Annotated[
        str,
        typer.Option(
            callback=server_host_prompt,
            help="endpoint of the server host",
        ),
    ],
    server_port: Annotated[
        int,
        typer.Option(
            callback=server_port_prompt,
            help="port of server host",
        ),
    ],
    server_log_level: Annotated[
        str,
        typer.Option(
            callback=server_log_level_prompt,
            help="log level of the server",
        ),
    ],
    cli_table_width: Annotated[
        Optional[int | None],
        typer.Option(
            help="CLI table width",
        ),
    ] = None,
    config: Path = typer.Option(
        default_config,
        callback=conf_callback,
        is_eager=True,
        help="path to config file that will be created",
    ),
):
    storage_settings = StorageSettings(location=storage_location, create=storage_create)
    server_settings = ServerSettings(
        host=server_host, port=server_port, log_level=server_log_level
    )
    cli_table_settings = CLITableSettings(width=cli_table_width)
    cli_settings = CLISettings(table=cli_table_settings)
    settings = Settings(
        storage=storage_settings,
        server=server_settings,
        cli=cli_settings,
    )
    with open(config, "w") as fd:
        yaml.dump(settings.model_dump(), fd)
