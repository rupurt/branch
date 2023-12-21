import importlib
from .main import app

importlib.import_module("branch.cli.server.start")


if __name__ == "__main__":
    app()
