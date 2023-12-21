from typing import Optional
from pydantic import BaseModel, Field


class Retention(BaseModel):
    bytes: Optional[int] = Field(ge=1, default=None)
    ms: Optional[int] = Field(ge=1, default=None)

    def model_dump(self, *args, **kwargs) -> dict[str, int]:
        return super().model_dump(exclude_none=True)
