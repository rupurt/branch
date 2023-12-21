import pytest
from result import is_ok
from branch.testing import invoke_cli
import branch.core


@pytest.fixture
def my_topic_a():
    return "my-topic.a"


@pytest.fixture
def msg():
    return '{"hello":"world"}'


@pytest.fixture(autouse=True)
def setup_produce(local_adapter, my_topic_a):
    assert is_ok(
        branch.core.create_topic(name=my_topic_a, partitions=2, storage=local_adapter)
    )
    assert is_ok(
        branch.core.create_topic(name="my-topic.b", partitions=1, storage=local_adapter)
    )


@pytest.mark.skip()
def test_produce_success(
    local_adapter,
    storage_location,
    my_topic_a,
    msg,
):
    result = invoke_cli(
        f"""\
        produce \
            --topic='{my_topic_a}' \
            --partition=0 \
            --message='{msg}' \
            --storage-location='{storage_location}'
        """,
    )
    assert result.exit_code == 0
    assert result.stdout == ""

    consume_result = branch.consume(my_topic_a, max_records=1, storage=local_adapter)
    assert is_ok(consume_result)
    records = consume_result.ok()
    assert len(records) == 1


@pytest.mark.skip()
def test_produce_verbose_success(
    local_adapter,
    storage_location,
    my_topic_a,
    msg,
):
    result = invoke_cli(
        f"""\
        produce \
            --topic='{my_topic_a}' \
            --partition=0 \
            --message='{msg}' \
            --verbose \
            --storage-location='{storage_location}'
        """,
    )
    assert result.exit_code == 0
    assert msg in result.stdout

    consume_result = branch.consume(my_topic_a, max_records=1, storage=local_adapter)
    assert is_ok(consume_result)
    records = consume_result.ok()
    assert len(records) == 1


def test_produce_missing_arguments_error():
    result = invoke_cli("produce")
    assert result.exit_code == 2
    assert "Error" in result.stdout
    assert "Missing option '--topic'" in result.stdout


def test_list_unsupported_storage_location_error():
    result = invoke_cli(
        f"""\
        produce \
            --topic='{my_topic_a}' \
            --partition=0 \
            --message='{msg}' \
            --storage-location='foo://bar.com'
        """,
    )
    assert result.exit_code == 2
    assert "unsupported protocol in location 'foo://bar.com'" in result.stdout
