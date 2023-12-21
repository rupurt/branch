from typing import Optional, TypeAlias
from pydantic import BaseModel, Field
from branch.core.records.base import RecordKey, RecordHeaders, RecordValueId
from branch.core.topics.offset_manifest import OffsetManifest

OffsetNumber: TypeAlias = int


class Offset(BaseModel):
    number: OffsetNumber = Field()
    key: Optional[RecordKey] = Field()
    headers: RecordHeaders = Field()
    value_id: RecordValueId = Field()

    def to_manifest(self) -> OffsetManifest:
        manifest = OffsetManifest(
            key=self.key,
            headers=self.headers,
            value_id=self.value_id,
        )
        return manifest
