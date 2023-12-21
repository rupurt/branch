from result import Result, Ok, Err
from branch.core.storage.abc_storage_adapter import ABCStorageAdapter
from branch.core.records.consumer_record import ConsumerRecord


def consume(
    topic: str,
    max_records: int,
    storage: ABCStorageAdapter,
) -> Result[list[ConsumerRecord], type[NotImplementedError]]:
    glob_result = storage.glob(f"topics/{topic}/partitions/*/offsets/*.manifest.json")
    if isinstance(glob_result, Err):
        return Err(glob_result.err())
    consumer_records: list[ConsumerRecord] = []
    return Ok(consumer_records)
