import importlib
from branch import feature
from .main import app

importlib.import_module("branch.cli.init")
importlib.import_module("branch.cli.produce")
importlib.import_module("branch.cli.consume")

topics = importlib.import_module("branch.cli.topics")
app.add_typer(topics.app, name="topics")

server = importlib.import_module("branch.cli.server")
app.add_typer(server.app, name="server")

if feature.TUI_ENABLED:
    tui = importlib.import_module("branch.cli.tui")
    importlib.import_module("branch.cli.tui")

if __name__ == "__main__":
    app()
