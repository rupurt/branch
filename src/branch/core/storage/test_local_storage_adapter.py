import os
from pathlib import Path
import pytest
from result import is_ok, is_err
from .local_storage_adapter import LocalStorageAdapter


@pytest.fixture()
def adapter(tmp_path):
    return LocalStorageAdapter(f"local://{tmp_path}")


@pytest.fixture()
def my_object_key():
    return "my-object"


@pytest.fixture()
def my_data():
    return b"my-data"


@pytest.fixture()
def setup_my_object(tmp_path, my_object_key, my_data):
    with open(f"{tmp_path}/{my_object_key}", mode="wb") as fd:
        fd.write(my_data)


@pytest.fixture()
def my_nested_object_key():
    return "my-nested/hello.txt"


@pytest.fixture()
def my_nested_data():
    return b"my-nested-data"


@pytest.fixture()
def setup_my_other_object(tmp_path, my_nested_object_key, my_nested_data):
    absolute_key = f"{tmp_path}/{my_nested_object_key}"
    parent = Path(absolute_key).parent
    os.mkdir(parent)
    with open(absolute_key, mode="wb") as fd:
        fd.write(my_nested_data)


def test_put_success(
    adapter,
    tmp_path,
    my_object_key,
    my_data,
):
    result = adapter.put(key=my_object_key, content=my_data)
    assert is_ok(result)
    with open(f"{tmp_path}/{my_object_key}", mode="rb") as fd:
        assert fd.read() == my_data


def test_put_creates_subdirectories(
    adapter,
    tmp_path,
    my_data,
):
    result = adapter.put(key="foo/bar/baz.txt", content=my_data)
    assert is_ok(result)
    with open(f"{tmp_path}/foo/bar/baz.txt", mode="rb") as fd:
        assert fd.read() == my_data


@pytest.mark.skip()
def test_put_unique_key_error(
    adapter,
    tmp_path,
    my_object_key,
    my_data,
):
    result = adapter.put(key=my_object_key, content=my_data)
    assert is_ok(result)
    result = adapter.put(key=my_object_key, content=my_data)
    assert is_err(result)
    # assert not os.path.exists(f"{tmp_path}/{my_object_key}")


def test_get_success(
    setup_my_object,
    adapter,
    my_object_key,
    my_data,
):
    result = adapter.get(key=my_object_key)
    assert result.ok() == my_data


def test_get_not_found_error(adapter):
    result = adapter.get(key="not-found")
    assert is_err(result)
    assert isinstance(result.err_value, FileNotFoundError)
    assert "No such file or directory" in str(result.err_value)


def test_glob_success(
    setup_my_object,
    setup_my_other_object,
    adapter,
    my_object_key,
    my_nested_object_key,
):
    result = adapter.glob(pattern="**")
    keys = result.ok()
    assert len(keys) == 2
    assert keys[0] == my_nested_object_key
    assert keys[1] == my_object_key


def test_delete_success(
    setup_my_object,
    setup_my_other_object,
    tmp_path,
    adapter,
    my_object_key,
    my_nested_object_key,
):
    result = adapter.delete(key=my_object_key)
    assert is_ok(result)
    assert os.path.exists(f"{tmp_path}/{my_object_key}") is False
    assert os.path.exists(f"{tmp_path}/{my_nested_object_key}") is True
