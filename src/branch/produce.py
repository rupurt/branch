import json
from typing import Any
from result import Result, Ok, Err
from branch.core.storage.abc_storage_adapter import ABCStorageAdapter
from branch.core.records.producer_record import ProducerRecord
from branch.core.topics.topic_cache import next_offset
from branch.core.topics.offset import Offset, OffsetNumber


def produce(
    record: ProducerRecord, storage: ABCStorageAdapter, **kwargs
) -> Result[Offset, type[NotImplementedError] | Any]:
    record_result = __put_record_value__(record, storage)
    if isinstance(record_result, Err):
        return Err(record_result.err())
    next = kwargs.get("next_offset") or next_offset
    (offset_result, offset) = __put_offset__(record, next(record.topic), storage)
    if isinstance(offset_result, Err):
        return Err(offset_result.err())
    return Ok(offset)


def __put_record_value__(record: ProducerRecord, storage: ABCStorageAdapter):
    result = storage.put(record.value_key(), record.value)
    return result


def __put_offset__(
    record: ProducerRecord, number: OffsetNumber, storage: ABCStorageAdapter
):
    offset = Offset(
        number=number, key=record.key, headers=record.headers, value_id=record.value_id
    )
    offset_manifest = offset.to_manifest()
    offset_manifest_content = json.dumps(offset_manifest.model_dump(), default=str)
    partitions_path = f"_topics/{record.topic}/partitions/{record.partition}"
    offset_manifest_key = f"{partitions_path}/offsets/{number}.manifest.json"
    result = storage.put(offset_manifest_key, offset_manifest_content.encode())
    return (result, offset)
