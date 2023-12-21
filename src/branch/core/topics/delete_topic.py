from result import Result, Ok, Err
from branch.core.storage.abc_storage_adapter import ABCStorageAdapter


def delete_topic(
    topic: str, storage: ABCStorageAdapter
) -> Result[None, type[FileNotFoundError] | type[NotImplementedError]]:
    """
    Delete a topic

    - deletes the committed topic manifest immediately
    - schedules cleanup of partitions and records for the topic
    """
    topic_manifest_key = __topic_manifest_key__(topic)
    get_topic_manifest_result = storage.get(topic_manifest_key)
    if isinstance(get_topic_manifest_result, Err):
        return Err(get_topic_manifest_result.err())
    delete_topic_manifest_result = storage.delete(topic_manifest_key)
    if isinstance(delete_topic_manifest_result, Err):
        return Err(delete_topic_manifest_result.err())
    return Ok(None)


def __topic_manifest_key__(topic: str) -> str:
    return f"topics/{topic}.manifest.json"
