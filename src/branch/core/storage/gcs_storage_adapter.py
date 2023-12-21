from typing import Any
from result import Ok
import fsspec
from .abc_storage_adapter import ABCStorageAdapter


class GCSStorageAdapter(ABCStorageAdapter):
    """
    Manage persistence on a `Google Cloud Storage` bucket and optional prefix defined in the given `location`
    """

    fs: Any

    def __init__(self, location: str):
        self.fs = fsspec.filesystem("gcs")

    def put(self, key: str, content: bytes):
        return Ok(None)

    def get(self, key: str):
        return Ok(b"")

    def glob(self, pattern: str):
        return Ok([])

    def delete(self, key: str):
        return Ok(True)
