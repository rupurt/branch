from typing import Optional
from pydantic import BaseModel, Field
from branch.core.records.base import RecordKey, RecordHeaders, RecordValueId


class OffsetManifest(BaseModel):
    key: Optional[RecordKey] = Field()
    headers: RecordHeaders = Field()
    value_id: RecordValueId = Field()
