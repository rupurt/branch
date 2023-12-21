import typer
from typing_extensions import Annotated
from pathlib import Path
from branch.config import default_config, read_settings
from branch.cli.server import app


def conf_callback(ctx: typer.Context, param: typer.CallbackParam, value: str):
    ctx.default_map = ctx.default_map or {}
    if value:
        try:
            settings = read_settings(value)
            default_map = {
                "host": settings.server.host,
                "port": settings.server.port,
                "ui_port": settings.server.ui_port,
                "log_level": settings.server.log_level,
            }
            ctx.default_map.update(default_map)
        except Exception:
            pass
    return value


@app.command()
def start(
    host: Annotated[str, typer.Option(help="listen on host")],
    port: Annotated[int, typer.Option(help="api port")],
    ui_port: Annotated[int, typer.Option(help="web ui port")],
    log_level: Annotated[str, typer.Option(help="log level")],
    config: Path = typer.Option(
        default_config,
        callback=conf_callback,
        is_eager=True,
        help="path to config file",
    ),
):
    import branch.core

    settings = branch.core.ServerSettings(
        host=host,
        port=port,
        ui_port=ui_port,
        log_level=log_level,
    )
    branch.core.run_server(settings)


if __name__ == "__main__":
    app()
