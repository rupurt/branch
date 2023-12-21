import pytest
from result import is_ok
from branch.testing import invoke_cli
import branch.core


@pytest.fixture
def my_topic_a():
    return "my-topic.a"


@pytest.fixture(autouse=True)
def setup_consume(local_adapter, my_topic_a):
    assert is_ok(
        branch.core.create_topic(name=my_topic_a, partitions=2, storage=local_adapter)
    )
    assert is_ok(
        branch.core.create_topic(name="my-topic.b", partitions=1, storage=local_adapter)
    )


@pytest.mark.skip()
def test_consume_success(storage_location, my_topic_a):
    # topics.produce("my-topic.a", '{"hello":"world"}'

    result = invoke_cli(
        f"""\
        consume \
            --topic='{my_topic_a}' \
            --storage-location='{storage_location}'
        """,
    )
    assert result.exit_code == 0
    assert '{"hello":"world"}' in result.stdout


def test_consume_missing_arguments_error():
    result = invoke_cli("consume")
    assert result.exit_code == 2
    assert "Error" in result.stdout
    assert "Missing option '--topic'" in result.stdout


def test_unsupported_storage_location_error(my_topic_a):
    result = invoke_cli(
        f"""\
        consume \
            --topic='{my_topic_a}' \
            --storage-location='foo://bar.com'
        """,
    )
    assert result.exit_code == 2
    assert "unsupported protocol in location 'foo://bar.com'" in result.stdout
