from datetime import datetime
from pydantic import BaseModel, Field
from .partition_manifest import PartitionManifest

MIN_PARTITIONS = 1
MAX_PARTITIONS = 200_000
MIN_PARTITION_NUMBER = MIN_PARTITIONS - 1
MAX_PARTITION_NUMBER = MAX_PARTITIONS - 1


class Partition(BaseModel):
    number: int = Field(ge=MIN_PARTITION_NUMBER, le=MAX_PARTITION_NUMBER)
    created_at: datetime
    updated_at: datetime

    def to_manifest(self) -> PartitionManifest:
        manifest = PartitionManifest(
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
        return manifest
