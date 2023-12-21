from result import Result, Ok, Err
from branch.core.storage.abc_storage_adapter import ABCStorageAdapter
from branch.core.topics.topic import Topic
from branch.core.topics.topic_manifest import TopicManifest


def glob_topics(
    pattern: str, storage: ABCStorageAdapter
) -> Result[list[Topic], type[FileNotFoundError] | type[NotImplementedError]]:
    """
    List of topics with a name matching the glob `pattern`

    - supports wildcard `*`
    """
    manifest_keys_result = storage.glob(f"topics/{pattern}.manifest.json")
    if isinstance(manifest_keys_result, Err):
        return Err(manifest_keys_result.err())
    topics: list[Topic] = []
    for manifest_key in manifest_keys_result.ok():
        manifest_content_result = storage.get(manifest_key)
        if isinstance(manifest_content_result, Err):
            return Err(manifest_content_result.err())
        name = __topic_name_from_manifest_key__(manifest_key)
        manifest = TopicManifest.model_validate_json(manifest_content_result.ok())
        topic = Topic(
            name=name,
            partitions=manifest.partitions,
            retention=manifest.retention,
            created_at=manifest.created_at,
            updated_at=manifest.updated_at,
        )
        topics.append(topic)
    return Ok(topics)


def __topic_name_from_manifest_key__(key: str) -> str:
    return key.replace("topics/", "", 1).replace(".manifest.json", "", 1)
