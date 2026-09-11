from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .player import Player


class CreateClub(BaseModel):
    name: str


class Club(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None
    name: str
    admins: List["Player"] = Field(default_factory=list)
    players: List["Player"] = Field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None
