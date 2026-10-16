from __future__ import annotations
from datetime import datetime
from uuid import UUID
from pydantic.alias_generators import to_camel
from pydantic import field_serializer
import uuid

from pydantic import BaseModel, ConfigDict


class Player(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True
    )


class CreatePlayer(Player):
    first_name: str
    last_name: str


class ReadPlayer(Player):
    id: uuid.UUID | None = None
    name: str

    @field_serializer("name")
    def serialize_name(self, value: str) -> str:
        return value.title()

    rank: int = 0
    games_won: int = 0
    games_lost: int = 0
    sets_won: int = 0
    sets_lost: int = 0
    matches_played: int = 0
    created_at: datetime | None = None
    updated_at: datetime | None = None
