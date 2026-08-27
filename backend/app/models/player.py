from typing import List, TYPE_CHECKING

from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.db.schema import Base
from sqlalchemy import String, Integer, DateTime, func, Uuid
from datetime import datetime
from app.models.club import club_admin, club_player
from app.models.schemas import Player
import uuid

if TYPE_CHECKING:
    from app.models.club import ClubORM
    from app.models.team import TeamORM


class PlayerORM(Base):
    __tablename__ = "players"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, default=uuid.uuid4)
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

    admin_clubs: Mapped[List["ClubORM"]] = relationship(
        secondary=club_admin,
        back_populates="admins"
    )
    clubs: Mapped[List["ClubORM"]] = relationship(
        secondary=club_player,
        back_populates="players"
    )
    teams: Mapped[List["TeamORM"]] = relationship(
        secondary="team_player",
        back_populates="players"
    )

    def __repr__(self):
        return f"<Player(id={self.id}, name={self.name})>"
