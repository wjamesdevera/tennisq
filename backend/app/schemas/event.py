from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, date as date_type
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .club import Club
    from .match_log import MatchLog


class CreateEvent(BaseModel):
    name: str
    type: str
    date: str = datetime.now().date()
    club_id: int = None


class Event(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str | None = None
    name: str
    type: str
    date: date_type | None = datetime.now()
    club_id: int | None = None
    club: Club | None = None
    match_logs: List["MatchLog"] = Field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None
