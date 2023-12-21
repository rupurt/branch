from .main import app
from . import create  # noqa: F401
from . import list  # noqa: F401
from . import update  # noqa: F401
from . import delete  # noqa: F401

if __name__ == "__main__":
    app()
