from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, date as date_type
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .match_log import MatchLog


class CreateEvent(BaseModel):
    name: str
    type: str
    date: str = datetime.now().date()


class Event(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str | None = None
    name: str
    description: str
    max_players: int
    date: date_type | None = datetime.now()
    match_logs: List["MatchLog"] = Field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None
