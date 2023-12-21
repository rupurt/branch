import json
from typing import Optional
from datetime import datetime
from pydantic import ValidationError
from result import is_err, Result, Ok, Err
from branch.core.errors import UniqueError
from branch.core.topics.topic import Topic
from branch.core.topics.retention import Retention
from branch.core.storage.abc_storage_adapter import ABCStorageAdapter
from ._create_partition import create_partition


def create_topic(
    name: str,
    partitions: int,
    storage: ABCStorageAdapter,
    retention: Optional[Retention] = None,
) -> Result[Topic, ValidationError | UniqueError | type[NotImplementedError]]:
    """
    Save a new topic in persistent storage

    - create an internal `id` for the new topic which will store the partition manifests & record offsets/values
    - partition manifests will be saved to `_topics/{id}/partitions/{partition_number}/manifest.json`
    - once all partition manifests are successfully saved a topic manifest is committed
    - topic manifest will be saved to `topics/{topic_name}.manifest.json`
    - records can be produced and consumed once the topic manifest is committed
    - topic deletion is expressed as an `O(1)` operation by deleting the topic manifest
    - topic cleanup complexity varies by storage adapter up to `O(n)` where `n` is the number of committed records
    - topic cleanup can be executed as a background process
    - a `ValidationError` is returned when the topic attributes fail Pydantic validations
    - a `UniqueError` is returned when the topic already exists
    """
    now = datetime.now()
    try:
        topic = Topic(
            name=name,
            partitions=partitions,
            retention=retention,
            created_at=now,
            updated_at=now,
        )
    except ValidationError as err:
        return Err(err)
    for num in range(partitions):
        create_partition_result = create_partition(topic, num, storage)
        if is_err(create_partition_result):
            return Err(create_partition_result.err())
    put_topic_result = __put_topic_manifest__(topic, storage)
    if isinstance(put_topic_result, Err):
        return Err(put_topic_result.err())
    return Ok(topic)


def __put_topic_manifest__(topic: Topic, storage: ABCStorageAdapter):
    topic_manifest_key = __topic_manifest_key__(topic)
    topic_manifest_content = __topic_manifest_content__(topic)
    return storage.put(topic_manifest_key, topic_manifest_content)


def __topic_manifest_key__(topic: Topic) -> str:
    return f"topics/{topic.name}.manifest.json"


def __topic_manifest_content__(topic: Topic) -> bytes:
    manifest = topic.to_manifest()
    content = json.dumps(manifest.model_dump(), default=str)
    return content.encode()
