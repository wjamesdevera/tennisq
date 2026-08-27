from app.db.schema import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Integer, DateTime, func, Table, Column, ForeignKey
from datetime import datetime
from pydantic import BaseModel
from typing import List
from app.models.player import Player

team_player_table = Table(
    "team_player",
    Base.metadata,
    Column("team_id", ForeignKey("teams.id"), primary_key=True),
    Column("player_id", ForeignKey("players.id"), primary_key=True),
)


class TeamORM(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationship
    players: Mapped[List["Player"]] = relationship(
        secondary=team_player_table, back_populates="players")

    def __repr__(self):
        return f"<Team(id={self.id}, name={self.name})>"


class Team(BaseModel):
    id: int
    name: str
    players: List["Player"]
    created_at: datetime | None
    updated_at: datetime | None
