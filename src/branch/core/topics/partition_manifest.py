from datetime import datetime
from pydantic import BaseModel


class PartitionManifest(BaseModel):
    created_at: datetime
    updated_at: datetime
