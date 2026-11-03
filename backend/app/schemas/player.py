from __future__ import annotations
from datetime import datetime
from uuid import UUID
from pydantic.alias_generators import to_camel
from pydantic import field_serializer, field_validator, Field
import uuid
import re

from pydantic import BaseModel, ConfigDict

SQL_INJECTION_PATTERN = re.compile(
    # statement separators, comments
    r"(;|--|/\*|\*/|\bxp_\w+)"
    r"|\b(drop|delete|insert|update|alter|truncate|union|select|exec)\b"
    # keyword followed by something
    r"\s+\w",
    re.IGNORECASE,
)


class Player(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True
    )


class CreatePlayer(Player):
    first_name: str = Field(min_length=1, max_length=200)
    last_name: str = Field(min_length=1, max_length=200)

    @field_validator("first_name", "last_name")
    @classmethod
    def reject_html_characters(cls, value: str) -> str:
        if re.search(r"[<>]", value):
            raise ValueError("must not contain '<' or '>'")
        return value

    @field_validator("first_name", "last_name")
    @classmethod
    def reject_blank_space(cls, value: str) -> str:
        if value.strip() == "":
            raise ValueError("must not be blank")
        return value

    @field_validator("first_name", "last_name")
    @classmethod
    def reject_sql_injection(cls, value: str) -> str:
        if SQL_INJECTION_PATTERN.search(value):
            raise ValueError("contains disallowed SQL characters or keywords")
        return value


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
