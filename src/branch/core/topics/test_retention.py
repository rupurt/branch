from typing import Optional
from pydantic import ValidationError
from .retention import Retention


def test_validate_success():
    retention = __new_retention__(bytes=1000, ms=2000)
    assert isinstance(retention, Retention)
    assert retention.bytes == 1000
    assert retention.ms == 2000


def test_defaults():
    retention = Retention()
    assert retention.bytes is None
    assert retention.ms is None


def test_validate_bytes_minimum():
    try:
        __new_retention__(bytes=0)
    except ValidationError as err:
        errors = ValidationError.errors(err)
        assert len(errors) == 1
        error = errors[0]
        assert error["msg"] == "Input should be greater than or equal to 1"
    else:
        raise AssertionError("expected a ValidationError to be raised")


def test_validate_ms_minimum():
    try:
        __new_retention__(ms=0)
    except ValidationError as err:
        errors = ValidationError.errors(err)
        assert len(errors) == 1
        error = errors[0]
        assert error["msg"] == "Input should be greater than or equal to 1"
    else:
        raise AssertionError("expected a ValidationError to be raised")


def test_model_dump_excludes_empty_fields():
    retention = __new_retention__(bytes=None, ms=None)
    assert retention.model_dump() == {}


def __new_retention__(
    bytes: Optional[int] = None, ms: Optional[int] = None
) -> Retention:
    return Retention(bytes=bytes, ms=ms)
