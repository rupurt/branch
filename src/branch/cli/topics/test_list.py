import pytest
from result import is_ok
from branch.testing import invoke_cli
import branch.core


@pytest.fixture(autouse=True)
def setup_list(local_adapter):
    assert is_ok(
        branch.core.create_topic(
            name="my-topic.a.v1",
            partitions=2,
            retention=branch.core.Retention(bytes=1000),
            storage=local_adapter,
        )
    )
    assert is_ok(
        branch.core.create_topic(
            name="my-topic.b.v1",
            partitions=1,
            retention=branch.core.Retention(ms=2000),
            storage=local_adapter,
        )
    )
    assert is_ok(
        branch.core.create_topic(
            name="my-topic.b.v2",
            partitions=2,
            storage=local_adapter,
        )
    )


def test_list_success(storage_location):
    result = invoke_cli(
        f"""\
        topics list '*' \
            --storage-location='{storage_location}'
        """,
    )
    assert result.exit_code == 0
    assert "my-topic.a.v1" in result.stdout
    assert "bytes=1000" in result.stdout
    assert "my-topic.b.v1" in result.stdout
    assert "ms=2000" in result.stdout
    assert "my-topic.b.v2" in result.stdout


def test_list_missing_arguments_error():
    result = invoke_cli("topics list")
    assert result.exit_code == 2
    assert "Error" in result.stdout
    assert "Missing argument 'PATTERN'" in result.stdout


def test_list_unsupported_storage_location_error():
    result = invoke_cli(
        """\
        topics list '*' \
            --storage-location foo://bar.com
        """,
    )
    assert result.exit_code == 2
    assert "unsupported protocol in location 'foo://bar.com'" in result.stdout
