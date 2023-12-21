import json
from datetime import datetime
from result import is_err, Result, Ok, Err
from branch.core.topics.topic import Topic
from branch.core.topics.partition import Partition
from branch.core.storage.abc_storage_adapter import ABCStorageAdapter


def create_partition(
    topic: Topic,
    number: int,
    storage: ABCStorageAdapter,
) -> Result[None, type[NotImplementedError]]:
    now = datetime.now()
    partition = Partition(
        number=number,
        created_at=now,
        updated_at=now,
    )
    put_partition_result = __put_partition_manifest__(topic, partition, storage)
    if is_err(put_partition_result):
        return Err(put_partition_result.err())
    return Ok(None)


def __put_partition_manifest__(
    topic: Topic, partition: Partition, storage: ABCStorageAdapter
):
    key = __partition_manifest_key__(topic, partition.number)
    content = __partition_manifest_content__(partition)
    return storage.put(key, content)


def __partition_manifest_key__(topic: Topic, number: int) -> str:
    return f"_topics/{topic.name}/partitions/{number}/manifest.json"


def __partition_manifest_content__(partition: Partition) -> bytes:
    manifest = partition.to_manifest()
    content = json.dumps(manifest.model_dump(), default=str)
    return content.encode()
