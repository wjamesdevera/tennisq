
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Category(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
