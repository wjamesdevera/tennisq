from typing import TYPE_CHECKING, List
import uuid

from app.db.schema import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Integer, DateTime, Date, Uuid, func, ForeignKey, Table, Column
from datetime import datetime

from app.models.match import MatchLogORM
from app.models.club import ClubORM

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
    type: Mapped[str] = mapped_column(String(200))
    date: Mapped[datetime] = mapped_column(Date, server_default=func.now())

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Foreign Key
    club_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("clubs.id", ondelete="CASCADE"),
        nullable=False
    )
    club: Mapped['ClubORM'] = relationship("ClubORM", back_populates="events")

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
