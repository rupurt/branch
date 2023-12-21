from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .retention import Retention
from .topic_manifest import TopicManifest
from .partition import MIN_PARTITIONS, MAX_PARTITIONS


class Topic(BaseModel):
    """
    Durable record container with 1 or more partitions.

    - `name` is immutable and has a maximum length of 255 characters. The valid character set is `[a-Z1-9.-_]` with utf8 encoding
    - `partitions` is a positive integer with a maximum of `200,000`
    - `created_at` & `updated_at` are `datetime.datetime` objects
    """

    name: str = Field(pattern=r"^[.a-zA-Z0-9-_]+$", max_length=255)
    partitions: int = Field(ge=MIN_PARTITIONS, le=MAX_PARTITIONS)
    retention: Optional[Retention] = Field(default=None)
    created_at: datetime = Field()
    updated_at: datetime = Field()

    def to_manifest(self) -> TopicManifest:
        manifest = TopicManifest(
            partitions=self.partitions,
            retention=self.retention,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
        return manifest
