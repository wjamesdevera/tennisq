from typing import List, TYPE_CHECKING

from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.db.schema import Base
from sqlalchemy import String, Integer, DateTime, func, Uuid
from datetime import datetime
from pydantic import BaseModel
from app.models.club import club_player
import uuid

if TYPE_CHECKING:
    from app.models.club import Club


class PlayerORM(Base):
    __tablename__ = "players"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, default=func.uuid_generate_v4())
    name: Mapped[str] = mapped_column(String(200))
    rank: Mapped[int] = mapped_column(Integer(), default=0)
    games_won: Mapped[int] = mapped_column(Integer(), default=0)
    games_lost: Mapped[int] = mapped_column(Integer(), default=0)
    sets_won: Mapped[int] = mapped_column(Integer(), default=0)
    sets_lost: Mapped[int] = mapped_column(Integer(), default=0)
    matches_played: Mapped[int] = mapped_column(Integer(), default=0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationship
    clubs: Mapped[List["Club"]] = relationship(
        secondary=club_player,
        back_populates="clubs"
    )

    def __repr__(self):
        return f"<Player(id={self.id}, name={self.name})>"


class Player(BaseModel):
    id: uuid.UUID
    name: str
    rank: int = 0
    games_won: int = 0
    games_lost: int = 0
    sets_won: int = 0
    sets_lost: int = 0
    matches_played: int = 0

    created_at: datetime | None
    updated_at: datetime | None
