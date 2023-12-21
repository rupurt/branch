import pytest
from result import is_ok
from branch.testing import invoke_cli
import branch.core


@pytest.fixture
def topic_name():
    return "my-topic.a.v1"


def test_create_success(storage_location, local_adapter, topic_name):
    result = invoke_cli(
        f"""\
        topics create \
            --name='{topic_name}' \
            --partitions=3 \
            --storage-location='{storage_location}'
        """,
    )
    assert result.exit_code == 0
    assert result.stdout == ""

    created_topics_result = branch.core.glob_topics("*", storage=local_adapter)
    assert is_ok(created_topics_result)
    created_topics = created_topics_result.ok_value
    assert len(created_topics) == 1
    assert created_topics[0].name == "my-topic.a.v1"
    assert created_topics[0].partitions == 3


def test_create_verbose_success(storage_location, topic_name):
    result = invoke_cli(
        f"""\
        topics create \
            --verbose \
            --name='{topic_name}' \
            --partitions=3 \
            --storage-location='{storage_location}'
        """
    )
    assert result.exit_code == 0
    assert "successfully created topic" in result.stdout
    assert '- name="my-topic.a.v1"' in result.stdout
    assert "- partitions=3" in result.stdout
    assert "- retention=infinite" in result.stdout
    assert "- created_at=" in result.stdout
    assert "- updated_at=" in result.stdout
    assert "- time=" in result.stdout


def test_create_missing_arguments_error():
    result = invoke_cli("topics create")
    assert result.exit_code == 2
    assert "Error" in result.stdout
    assert "Missing option '--name'" in result.stdout


def test_create_validation_error(storage_location):
    result = invoke_cli(
        f"""\
        topics create \
            --name='my-topic/a/v1' \
            --partitions=3 \
            --storage-location='{storage_location}'
        """
    )
    assert result.exit_code == 2
    assert "name string should match pattern" in result.stdout


def test_create_unsupported_adapter_error(topic_name):
    result = invoke_cli(
        f"""\
        topics create \
            --name='{topic_name}' \
            --partitions=3 \
            --storage-location='foo://unsupported'
        """
    )
    assert result.exit_code == 2
    assert "unsupported protocol in location 'foo://unsupported'" in result.stdout
