import pytest
from result import is_ok
import branch.core
from .delete_topic import delete_topic


@pytest.fixture()
def my_topic_a():
    return "my-topic.a"


@pytest.fixture(autouse=True)
def setup_list(local_adapter, my_topic_a):
    assert is_ok(
        branch.core.create_topic(name=my_topic_a, partitions=2, storage=local_adapter)
    )
    assert is_ok(
        branch.core.create_topic(name="my-topic.b", partitions=1, storage=local_adapter)
    )


def test_delete_topic_success(tmp_path, local_adapter, my_topic_a):
    delete_result = delete_topic(
        topic=my_topic_a,
        storage=local_adapter,
    )
    assert is_ok(delete_result)

    glob_topics_result = branch.core.glob_topics("*", storage=local_adapter)
    assert is_ok(glob_topics_result)
    topics = glob_topics_result.ok()
    assert len(topics) == 1
    assert topics[0].name == "my-topic.b"
