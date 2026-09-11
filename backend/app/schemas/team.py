
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .player import Player


class Team(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    players: List["Player"] = Field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None
