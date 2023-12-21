import pytest
from result import is_ok
import branch.core


@pytest.fixture(autouse=True)
def setup_topics(local_adapter):
    result_a = branch.core.create_topic(
        name="topicA",
        partitions=1,
        retention=branch.core.Retention(bytes=1000, ms=2000),
        storage=local_adapter,
    )
    assert is_ok(result_a)
    result_b = branch.core.create_topic(
        name="topicB",
        partitions=2,
        storage=local_adapter,
    )
    assert is_ok(result_b)


def test_glob_success(local_adapter):
    glob_topics_result = branch.core.glob_topics(pattern="*", storage=local_adapter)
    assert is_ok(glob_topics_result)
    glob_topics = glob_topics_result.ok()
    assert len(glob_topics) == 2
    assert glob_topics[0].name == "topicA"
    assert glob_topics[0].partitions == 1
    assert glob_topics[0].retention is not None
    assert glob_topics[0].retention.bytes == 1000
    assert glob_topics[0].retention.ms == 2000
    assert glob_topics[0].created_at is not None
    assert glob_topics[0].updated_at is not None
    assert glob_topics[1].name == "topicB"
    assert glob_topics[1].partitions == 2
    assert glob_topics[1].retention is None
    assert glob_topics[1].created_at is not None
    assert glob_topics[1].updated_at is not None
