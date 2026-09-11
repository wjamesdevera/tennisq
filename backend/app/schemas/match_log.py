from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .category import Category
    from .event import Event
    from .team import Team


class MatchLog(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category_id: int | None = None
    event_id: int | None = None
    team_a_id: int | None = None
    team_b_id: int | None = None
    team_a: Team | None = None
    team_b: Team | None = None
    event: Event | None = None
    category: Category | None = None
    sets: List["Set"] = Field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None


class Set(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    set_number: int
    team_a_score: int
    team_b_score: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    match_id: int | None = None
    match_log: MatchLog | None = None
