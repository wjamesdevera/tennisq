from typing import TYPE_CHECKING, List
import uuid

from app.db.schema import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship, validates
from sqlalchemy import Integer, String, DateTime, Date, Uuid, func, ForeignKey, Table, Column, CheckConstraint
from datetime import datetime

from app.models.match import MatchLogORM

if TYPE_CHECKING:
    from app.models.player import PlayerORM

event_player = Table(
    "event_player",
    Base.metadata,
    Column("event_id", ForeignKey("events.id"), primary_key=True),
    Column("player_id", ForeignKey("players.id"), primary_key=True),
)


class EventORM(Base):
    __tablename__ = "events"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(String(200))

    max_players: Mapped[int] = mapped_column(
        Integer, CheckConstraint('max_players >= 2 AND max_players <= 100'))

    @validates
    def validate_max_players(self, key, value):
        if not 2 <= value <= 100:
            raise ValueError(f'Invalid age {value}')
        return value

    date: Mapped[datetime] = mapped_column(Date, server_default=func.now())

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationship
    match_logs: Mapped[List["MatchLogORM"]] = relationship(
        "MatchLogORM", back_populates="event",
    )

    players: Mapped[List["PlayerORM"]] = relationship(
        secondary=event_player,
        back_populates="events"
    )

    def __repr__(self):
        return f"<Event(id={self.id}, name={self.name})>"
