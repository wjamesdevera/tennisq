from app.db.schema import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, DateTime, func, ForeignKey
from datetime import datetime
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.team import TeamORM
    from app.models.event import EventORM
    from app.models.category import CategoryORM


class MatchLogORM(Base):
    __tablename__ = "match_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Foreign Key
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey(
        "categories.id", ondelete="CASCADE"), nullable=False)

    event_id: Mapped[int] = mapped_column(Integer, ForeignKey(
        "events.id", ondelete="CASCADE"), nullable=False)

    team_a_id: Mapped[int] = mapped_column(Integer, ForeignKey(
        "teams.id", ondelete="CASCADE"), nullable=False)

    team_b_id: Mapped[int] = mapped_column(Integer, ForeignKey(
        "teams.id", ondelete="CASCADE"), nullable=False)

    # Relationship
    sets: Mapped[List["SetORM"]] = relationship(
        "SetORM", back_populates="match_log", cascade="all,delete-orphan"
    )

    category: Mapped['CategoryORM'] = relationship(
        "CategoryORM", back_populates="match_logs")

    event: Mapped['EventORM'] = relationship(
        "EventORM", back_populates="match_logs")

    team_a: Mapped['TeamORM'] = relationship(
        "TeamORM", foreign_keys=[team_a_id], back_populates="matches_as_team_a")

    team_b: Mapped['TeamORM'] = relationship(
        "TeamORM", foreign_keys=[team_b_id], back_populates="matches_as_team_b")

    def __repr__(self):
        return f"<Match(id={self.id}>"


class SetORM(Base):
    __tablename__ = "sets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    set_number: Mapped[int] = mapped_column(Integer, default=1)
    team_a_score: Mapped[int] = mapped_column(Integer, default=0)
    team_b_score: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Foreign key
    match_id: Mapped[int] = mapped_column(Integer, ForeignKey(
        "match_logs.id", ondelete="CASCADE"), nullable=False)

    # Relationship
    match_log: Mapped['MatchLogORM'] = relationship(
        "MatchLogORM", back_populates="sets")

    def __repr__(self):
        return f"<Set(id={self.id}, team_a={self.team_a_score}, team_b={self.team_b_score}>"
