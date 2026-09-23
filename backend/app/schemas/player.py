from __future__ import annotations
from datetime import datetime
from uuid import UUID
import uuid

from pydantic import BaseModel, ConfigDict


class AddPlayer(BaseModel):
    id: UUID


class CreatePlayer(BaseModel):
    name: str


class Player(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID | None = None
    name: str
    rank: int = 0
    games_won: int = 0
    games_lost: int = 0
    sets_won: int = 0
    sets_lost: int = 0
    matches_played: int = 0
    created_at: datetime | None = None
    updated_at: datetime | None = None
