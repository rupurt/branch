import pytest
from result import is_ok
from branch.testing import invoke_cli
import branch.core


@pytest.fixture
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


def test_delete_success(storage_location, local_adapter, my_topic_a):
    result = invoke_cli(
        f"""\
        topics delete '{my_topic_a}' \
            --storage-location='{storage_location}'
        """,
    )
    print(result.stdout)
    assert result.exit_code == 0
    assert result.stdout == ""

    glob_topics_result = branch.core.glob_topics("*", storage=local_adapter)
    assert is_ok(glob_topics_result)
    topics = glob_topics_result.ok()
    assert len(topics) == 1
    assert topics[0].name == "my-topic.b"


@pytest.mark.skip
def test_delete_success_verbose(storage_location, local_adapter, my_topic_a):
    result = invoke_cli(
        f"""\
        topics delete '{my_topic_a}' \
            --verbose \
            --storage-location='{storage_location}'
        """,
    )
    assert result.exit_code == 0
    assert "foo" in result.stdout


@pytest.mark.skip
def test_delete_not_found_error(storage_location, local_adapter, my_topic_a):
    result = invoke_cli(
        f"""\
        topics delete '{my_topic_a}' \
            --storage-location='{storage_location}'
        """,
    )
    assert result.exit_code == 2
    assert "foo" in result.stdout
