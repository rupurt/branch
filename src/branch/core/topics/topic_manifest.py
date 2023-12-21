from typing import Optional
import datetime
from pydantic import BaseModel, Field
from .retention import Retention


class TopicManifest(BaseModel):
    partitions: int = Field(ge=1, le=200_000)
    retention: Optional[Retention] = Field(default=None)
    created_at: datetime.datetime = Field()
    updated_at: datetime.datetime = Field()

    def model_dump(self, *args, **kwargs) -> dict[str, int]:
        return super().model_dump(exclude_none=True)
