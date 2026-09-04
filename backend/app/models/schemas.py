from __future__ import annotations

import uuid
from datetime import date as date_type, datetime

from pydantic import BaseModel, ConfigDict, Field


class Category(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    created_at: datetime | None = None
    updated_at: datetime | None = None


class Player(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID | None
    name: str
    rank: int = 0
    games_won: int = 0
    games_lost: int = 0
    sets_won: int = 0
    sets_lost: int = 0
    matches_played: int = 0
    clubs: list[Club] = Field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None


class Club(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None
    name: str
    admins: list[Player] = Field(default_factory=list)
    players: list[Player] = Field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None


class Team(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    players: list[Player] = Field(default_factory=list)
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
    sets: list[Set] = Field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None


class Event(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: str
    date: date_type | None = None
    match_logs: list[MatchLog] = Field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None


for model in (Category, Player, Club, Team, Set, MatchLog, Event):
    model.model_rebuild(_types_namespace=globals())
