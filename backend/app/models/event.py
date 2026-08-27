from typing import List

from app.db.schema import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Integer, DateTime, Date, func
from datetime import datetime
from pydantic import BaseModel

from app.models.match import MatchLog


class EventORM(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    type: Mapped[str] = mapped_column(String(200))
    date: Mapped[datetime] = mapped_column(Date, server_default=func.now())

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationship
    match_logs: Mapped[List["MatchLog"]] = relationship(
        "MatchLogORM", back_populates="match_logs",
    )

    def __repr__(self):
        return f"<Event(id={self.id}, name={self.name})>"


class Event(BaseModel):
    id: int
    name: str
    type: str
    date: datetime | None
    match_logs: List["MatchLog"] | None
    created_at: datetime | None
    updated_at: datetime | None
