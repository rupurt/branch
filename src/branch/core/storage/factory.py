from result import Ok, Err
from .abc_storage_adapter import ABCStorageAdapter
from .local_storage_adapter import LocalStorageAdapter
from .gcs_storage_adapter import GCSStorageAdapter


class LocationProtocol(str):
    def __eq__(self, other):
        return self.__contains__(other)


def create(location: str) -> Ok[ABCStorageAdapter] | Err[ValueError]:
    match LocationProtocol(location):
        case "file://":
            return Ok(LocalStorageAdapter(location=location))
        case "local://":
            return Ok(LocalStorageAdapter(location=location))
        case "gcs://":
            return Ok(GCSStorageAdapter(location=location))
        case "gs://":
            return Ok(GCSStorageAdapter(location=location))
        case _:
            return Err(ValueError(f"unsupported protocol in location '{location}'"))
