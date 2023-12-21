from datetime import datetime
from pydantic import ValidationError
from .partition import Partition


def test_validate_number_success():
    assert isinstance(__new_partition__(number=0), Partition)


def test_validate_number_range():
    try:
        __new_partition__(number=-1)
    except ValidationError as err:
        errors = ValidationError.errors(err)
        assert len(errors) == 1
        error = errors[0]
        assert error["msg"] == "Input should be greater than or equal to 0"
    else:
        raise AssertionError("expected a ValidationError to be raised")
    try:
        __new_partition__(number=200_000)
    except ValidationError as err:
        errors = ValidationError.errors(err)
        assert len(errors) == 1
        error = errors[0]
        assert error["msg"] == "Input should be less than or equal to 199999"
    else:
        raise AssertionError("expected a ValidationError to be raised")


def test_to_manifest():
    partition = __new_partition__(created_at=datetime.now(), updated_at=datetime.now())
    manifest = partition.to_manifest()
    assert manifest.created_at == partition.created_at
    assert manifest.updated_at == partition.updated_at


def __new_partition__(
    number: int = 0,
    created_at=datetime.now(),
    updated_at=datetime.now(),
) -> Partition:
    return Partition(
        number=number,
        created_at=created_at,
        updated_at=updated_at,
    )
