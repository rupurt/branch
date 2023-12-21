from pydantic import BaseModel, Field
from uuid_extensions import uuid7
from .base import RecordKey, RecordHeaders, RecordValueId


def __value_id__() -> RecordValueId:
    return int(repr(uuid7(as_type="int")))


class ProducerRecord(BaseModel):
    topic: str = Field()
    partition: int = Field()
    key: RecordKey = Field(default=None)
    headers: RecordHeaders = Field(default={})
    value_id: RecordValueId = Field(default=__value_id__())
    value: bytes = Field()

    def value_key(self) -> str:
        return (
            f"_topics/{self.topic}/partitions/{self.partition}/values/{self.value_id}"
        )
