from typing import Optional
from datetime import datetime
from pydantic import ValidationError
from .topic import Topic
from .retention import Retention


def test_validate_name_success():
    topic = __new_topic__(name="my-topic")
    assert isinstance(topic, Topic)
    assert topic.name == "my-topic"
    assert topic.retention is None


def test_validate_name_pattern():
    try:
        __new_topic__(name="")
    except ValidationError as err:
        errors = ValidationError.errors(err)
        assert len(errors) == 1
        error = errors[0]
        assert error["msg"] == r"String should match pattern '^[.a-zA-Z0-9-_]+$'"
    else:
        raise AssertionError("expected a ValidationError to be raised")
    try:
        __new_topic__(name=" ")
    except ValidationError as err:
        errors = ValidationError.errors(err)
        assert len(errors) == 1
        error = errors[0]
        assert error["msg"] == r"String should match pattern '^[.a-zA-Z0-9-_]+$'"
    else:
        raise AssertionError("expected a ValidationError to be raised")
    try:
        __new_topic__(name="hello/world")
    except ValidationError as err:
        errors = ValidationError.errors(err)
        assert len(errors) == 1
        error = errors[0]
        assert error["msg"] == r"String should match pattern '^[.a-zA-Z0-9-_]+$'"
    else:
        raise AssertionError("expected a ValidationError to be raised")


def test_validate_name_max_length():
    topic_name = __topic_name__(value="a", repeat=256)
    try:
        __new_topic__(name=topic_name)
    except ValidationError as err:
        errors = ValidationError.errors(err)
        assert len(errors) == 1
        error = errors[0]
        assert error["msg"] == "String should have at most 255 characters"
    else:
        raise AssertionError("expected a ValidationError to be raised")


def test_validate_partitions_success():
    assert isinstance(__new_topic__(partitions=1), Topic)


def test_validate_partitions_range():
    try:
        __new_topic__(partitions=0)
    except ValidationError as err:
        errors = ValidationError.errors(err)
        assert len(errors) == 1
        error = errors[0]
        assert error["msg"] == "Input should be greater than or equal to 1"
    else:
        raise AssertionError("expected a ValidationError to be raised")
    try:
        __new_topic__(partitions=200_001)
    except ValidationError as err:
        errors = ValidationError.errors(err)
        assert len(errors) == 1
        error = errors[0]
        assert error["msg"] == "Input should be less than or equal to 200000"
    else:
        raise AssertionError("expected a ValidationError to be raised")


def test_to_manifest():
    topic = __new_topic__()
    manifest = topic.to_manifest()
    assert manifest.partitions == topic.partitions
    assert manifest.created_at == topic.created_at
    assert manifest.updated_at == topic.updated_at
    assert manifest.retention is None


def __new_topic__(
    name: str = "my-topic",
    partitions: int = 1,
    retention: Optional[Retention] = None,
    created_at=datetime.now(),
    updated_at=datetime.now(),
) -> Topic:
    return Topic(
        name=name,
        retention=retention,
        partitions=partitions,
        created_at=created_at,
        updated_at=updated_at,
    )


def __topic_name__(value: str, repeat: int) -> str:
    return value * repeat
