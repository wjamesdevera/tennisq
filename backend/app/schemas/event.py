from __future__ import annotations
import uuid

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, date as date_type
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .match_log import MatchLog
    from .player import Player


class Event(BaseModel):
    name: str
    description: str
    max_players: int = Field(ge=2, le=50)
    date: date_type

    model_config = ConfigDict(from_attributes=True)
    # match_logs: List["MatchLog"] = Field(default_factory=list)
    # players: List["Player"] = Field(default_factory=list)


class CreateEvent(Event):
    pass


class ReadEvent(Event):
    id: uuid.UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None
