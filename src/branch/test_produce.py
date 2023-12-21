import json
import pytest
from result import is_ok, is_err
import branch.core


@pytest.fixture()
def topic_a():
    return "my-topic.a"


@pytest.fixture()
def topic_b():
    return "my-topic.b"


@pytest.fixture()
def msg():
    return b'{"hello":"world"}'


@pytest.fixture()
def partitions_path(tmp_path, topic_a):
    return f"{tmp_path}/_topics/{topic_a}/partitions"


def setup_produce(local_adapter, topic_a, topic_b):
    assert is_ok(
        branch.core.create_topic(name=topic_a, partitions=3, storage=local_adapter)
    )
    assert is_ok(
        branch.core.create_topic(name=topic_b, partitions=1, storage=local_adapter)
    )


def test_produce_success(local_adapter, topic_a, msg, partitions_path):
    record = branch.core.ProducerRecord(
        topic=topic_a,
        partition=0,
        key=None,
        headers={},
        value=msg,
    )
    produce_result = branch.produce(record, storage=local_adapter)
    assert is_ok(produce_result)

    with open(f"{partitions_path}/0/offsets/0.manifest.json", "rb") as fd:
        content = json.loads(fd.read())
        assert content["key"] is None
        assert content["headers"] == {}
        value_id = content["value_id"]
        assert value_id > 0
    with open(f"{partitions_path}/0/values/{value_id}", "rb") as fd:
        assert fd.read() == b'{"hello":"world"}'


@pytest.mark.skip()
def test_produce_partition_not_found_error(tmp_path, local_adapter, topic_a, msg):
    record = branch.core.ProducerRecord(
        topic=topic_a,
        partition=4,
        key=None,
        headers={},
        value=msg,
    )
    produce_result = branch.produce(record, storage=local_adapter)
    assert is_err(produce_result)
    assert 1 == 2
