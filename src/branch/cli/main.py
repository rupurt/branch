import typer
from branch.cli.utils import NaturalOrderGroup

app = typer.Typer(
    no_args_is_help=True,
    cls=NaturalOrderGroup,
)
