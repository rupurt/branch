from result import is_ok, is_err
from .local_storage_adapter import LocalStorageAdapter
from .gcs_storage_adapter import GCSStorageAdapter
from . import factory


def test_create():
    file_result = factory.create("file://.branch/foo")
    assert is_ok(file_result)
    assert isinstance(file_result.ok_value, LocalStorageAdapter)
    local_result = factory.create("local://.branch/foo")
    assert is_ok(local_result)
    assert isinstance(local_result.ok_value, LocalStorageAdapter)
    gcs_result = factory.create("gcs://my-bucket")
    assert is_ok(gcs_result)
    assert isinstance(gcs_result.ok_value, GCSStorageAdapter)
    gs_result = factory.create("gs://my-bucket")
    assert is_ok(gs_result)
    assert isinstance(gs_result.ok_value, GCSStorageAdapter)
    unknown_result = factory.create("foo://my-bucket")
    assert is_err(unknown_result)
    assert isinstance(unknown_result.err_value, ValueError)
    assert (
        str(unknown_result.err_value)
        == "unsupported protocol in location 'foo://my-bucket'"
    )
