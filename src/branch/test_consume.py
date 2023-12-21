import pytest
from result import is_ok
import branch.core


@pytest.fixture
def my_topic_a():
    return "my-topic.a"


@pytest.fixture(autouse=True)
def setup_produce(local_adapter, my_topic_a):
    assert is_ok(
        branch.core.create_topic(name=my_topic_a, partitions=2, storage=local_adapter)
    )
    assert is_ok(
        branch.core.create_topic(name="my-topic.b", partitions=1, storage=local_adapter)
    )


@pytest.mark.skip
def test_consume_success(local_adapter, my_topic_a):
    produce_result_1 = __produce__(my_topic_a, 0, b"record 1", local_adapter)
    assert is_ok(produce_result_1)
    produce_result_2 = __produce__(my_topic_a, 0, b"record 2", local_adapter)
    assert is_ok(produce_result_2)
    produce_result_3 = __produce__(my_topic_a, 0, b"record 3", local_adapter)
    assert is_ok(produce_result_3)

    consume_result = branch.consume(my_topic_a, max_records=2, storage=local_adapter)
    assert is_ok(consume_result)
    consumer_records = consume_result.ok()
    assert len(consumer_records) == 2


def __produce__(
    topic: str,
    partition: int,
    value: bytes,
    local_adapter: branch.core.ABCStorageAdapter,
):
    record = branch.core.ProducerRecord(
        topic=topic,
        partition=partition,
        value=value,
    )
    return branch.produce(record, storage=local_adapter)
