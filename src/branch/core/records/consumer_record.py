from pydantic import BaseModel, Field
from .base import RecordKey, RecordHeaders, RecordValueId


class ConsumerRecord(BaseModel):
    topic: str = Field()
    partition: int = Field()
    key: RecordKey = Field()
    headers: RecordHeaders = Field()
    value_id: RecordValueId = Field()
    value: bytes = Field()
