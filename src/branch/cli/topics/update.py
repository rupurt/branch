import typer
from pathlib import Path
from branch.config import default_config
from .main import app


def conf_callback(ctx: typer.Context, param: typer.CallbackParam, value: str):
    ctx.default_map = ctx.default_map or {}
    if value:
        try:
            default_map = {}
            ctx.default_map.update(default_map)
        except Exception:
            pass
    return value


@app.command()
def update(
    config: Path = typer.Option(
        default_config,
        callback=conf_callback,
        is_eager=True,
        help="path to config file",
    ),
):
    print("TODO... topics update")
