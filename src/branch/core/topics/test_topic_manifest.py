from typing import Optional
from datetime import datetime
import pytest
from pydantic import ValidationError
from .topic_manifest import TopicManifest
from .retention import Retention


@pytest.fixture
def created_at():
    return datetime.now()


@pytest.fixture
def updated_at():
    return datetime.now()


def test_validate_success(created_at, updated_at):
    manifest = __new_manifest__(
        partitions=1,
        created_at=created_at,
        updated_at=updated_at,
    )
    assert manifest.partitions == 1
    assert manifest.created_at == created_at
    assert manifest.updated_at == updated_at
    assert manifest.retention is None


def test_validate_partition_range():
    try:
        __new_manifest__(partitions=0)
    except ValidationError as err:
        errors = ValidationError.errors(err)
        assert len(errors) == 1
        error = errors[0]
        assert error["msg"] == "Input should be greater than or equal to 1"
    else:
        raise AssertionError("expected a ValidationError to be raised")
    try:
        __new_manifest__(partitions=200_001)
    except ValidationError as err:
        errors = ValidationError.errors(err)
        assert len(errors) == 1
        error = errors[0]
        assert error["msg"] == "Input should be less than or equal to 200000"
    else:
        raise AssertionError("expected a ValidationError to be raised")


@pytest.mark.skip
def test_validate_created_at():
    assert 1 == 2


@pytest.mark.skip
def test_validate_updated_at():
    assert 1 == 2


def test_model_dump_excludes_empty_retention():
    manifest_with_empty_retention = __new_manifest__()
    assert "retention" not in manifest_with_empty_retention.model_dump()
    retention = Retention(bytes=1000, ms=2000)
    manifest_with_retention = __new_manifest__(retention=retention)
    dumped_manifest_with_retention = manifest_with_retention.model_dump()
    assert dumped_manifest_with_retention["retention"] == {
        "bytes": 1000,
        "ms": 2000,
    }


def __new_manifest__(
    partitions: int = 1,
    retention: Optional[Retention] = None,
    created_at: datetime = datetime.now(),
    updated_at: datetime = datetime.now(),
) -> TopicManifest:
    manifest = TopicManifest(
        partitions=partitions,
        retention=retention,
        created_at=created_at,
        updated_at=updated_at,
    )
    return manifest
