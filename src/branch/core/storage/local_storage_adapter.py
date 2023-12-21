from pathlib import Path
from result import Ok, Err
from fsspec import AbstractFileSystem
import fsspec
from .abc_storage_adapter import ABCStorageAdapter


class LocalStorageAdapter(ABCStorageAdapter):
    """
    Manage persistance on the local filesystem relative to the root
    directory of the `location`.
    """

    root_dir: str
    fs: AbstractFileSystem

    def __init__(self, location: str):
        self.root_dir = self.__location_root_dir__(location)
        self.fs = fsspec.filesystem("file")

    def put(self, key: str, content: bytes):
        absolute_path = self.__absolute_key__(key)
        parent = Path(absolute_path).parent
        if not self.fs.exists(parent):
            self.fs.mkdir(parent)
        with self.fs.open(absolute_path, mode="wb") as fd:
            fd.write(content)
        return Ok(None)

    def get(self, key: str):
        try:
            absolute_path = self.__absolute_key__(key)
            with self.fs.open(absolute_path, mode="rb") as fd:
                content = fd.read()
                return Ok(content)
        except FileNotFoundError as err:
            return Err(err)

    def glob(self, pattern: str):
        """
        Returns a list of keys matching the glob `pattern`. Valid wildcards are `*`, `**`, `?` & `[..]`

        - `pattern="*"` only searches the parent directory
        - `pattern="**"` recursively searches the directory hierachy
        - `pattern="?"` the previous character 0 or 1 times
        - `pattern="[..]"` set of characters to match
        """
        keys: list[str] = []
        absolute_key = self.__absolute_key__(pattern)
        glob_result = self.fs.glob(absolute_key)
        for path in glob_result:
            if isinstance(path, str) and not self.fs.isdir(path):
                key = self.__path_to_key__(path)
                keys.append(key)
        return Ok(keys)

    def delete(self, key: str):
        absolute_key = self.__absolute_key__(key)
        self.fs.delete(absolute_key)
        return Ok(True)

    def __location_root_dir__(self, location: str) -> str:
        local_location = location.replace("file://", "", 1).replace("local://", "", 1)
        path = Path(local_location)
        return str(path.absolute())

    def __absolute_key__(self, key: str) -> str:
        return f"{self.root_dir}/{key}"

    def __path_to_key__(self, path: str) -> str:
        return path.replace(self.root_dir, "").replace(self.fs.root_marker, "", 1)
