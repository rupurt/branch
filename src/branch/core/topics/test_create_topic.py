import json
import pytest
from pydantic import ValidationError
from result import is_ok, is_err
from .create_topic import create_topic
from .retention import Retention


@pytest.fixture()
def topic_name():
    return "my-topic.a.v1"


def test_create_topic_success(tmp_path, local_adapter, topic_name):
    create_result = create_topic(
        name=topic_name,
        partitions=2,
        storage=local_adapter,
    )
    assert is_ok(create_result)
    topic = create_result.ok_value
    assert topic.name == topic_name
    assert topic.partitions == 2
    assert topic.retention is None

    topic_manifests_result = local_adapter.glob("topics/*.manifest.json")
    assert is_ok(topic_manifests_result)
    topic_manifests = topic_manifests_result.ok()
    assert len(topic_manifests) == 1
    assert topic_manifests[0] == f"topics/{topic_name}.manifest.json"
    with open(f"{tmp_path}/{topic_manifests[0]}", "rb") as fd:
        manifest = json.loads(fd.read())
        assert manifest["partitions"] == 2
        assert manifest["created_at"] is not None
        assert manifest["updated_at"] is not None

    partition_manifests_result = local_adapter.glob(
        "_topics/*/partitions/*/manifest.json"
    )
    assert is_ok(partition_manifests_result)
    partition_manifests = partition_manifests_result.ok_value
    assert len(partition_manifests) == 2
    assert partition_manifests[0] == f"_topics/{topic_name}/partitions/0/manifest.json"
    with open(f"{tmp_path}/{partition_manifests[0]}", "rb") as fd:
        manifest = json.loads(fd.read())
        assert manifest["created_at"] is not None
        assert manifest["updated_at"] is not None
    assert partition_manifests[1] == f"_topics/{topic_name}/partitions/1/manifest.json"
    with open(f"{tmp_path}/{partition_manifests[1]}", "rb") as fd:
        manifest = json.loads(fd.read())
        assert manifest["created_at"] is not None
        assert manifest["updated_at"] is not None


def test_create_topic_with_retention_success(tmp_path, local_adapter, topic_name):
    retention = Retention(bytes=1000, ms=2000)
    create_result = create_topic(
        name=topic_name,
        partitions=2,
        retention=retention,
        storage=local_adapter,
    )
    assert is_ok(create_result)
    topic = create_result.ok_value
    assert topic.name == topic_name
    assert topic.retention is not None
    assert topic.retention.bytes == 1000
    assert topic.retention.ms == 2000


def test_create_topic_validation_error(local_adapter):
    result = create_topic(
        name="my-topic/a/v1",
        partitions=1,
        storage=local_adapter,
    )
    assert is_err(result)
    assert isinstance(result.err_value, ValidationError)
    errors = ValidationError.errors(result.err_value)
    assert len(errors) == 1
    assert "String should match pattern" in errors[0]["msg"]


@pytest.mark.skip()
def test_create_topic_unique_name_error(local_adapter, topic_name):
    result = create_topic(
        name=topic_name,
        partitions=1,
        storage=local_adapter,
    )
    assert is_ok(result)

    result = create_topic(
        name=topic_name,
        partitions=1,
        storage=local_adapter,
    )
    assert is_err(result)
    assert isinstance(result.err_value, ValueError)
    assert str(result.err_value) == "todo"


@pytest.mark.skip()
def test_create_topic_storage_error(topic_name, local_adapter):
    result = create_topic(
        name=topic_name,
        partitions=1,
        storage=local_adapter,
    )
    print(result)
    assert result == "todo"
