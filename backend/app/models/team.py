from app.db.schema import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Integer, DateTime, func, Table, Column, ForeignKey
from datetime import datetime
from typing import List, TYPE_CHECKING
from app.models.player import PlayerORM
from app.models.schemas import Team

if TYPE_CHECKING:
    from app.models.match import MatchLogORM

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
    players: Mapped[List["PlayerORM"]] = relationship(
        secondary=team_player_table, back_populates="teams")

    matches_as_team_a: Mapped[List["MatchLogORM"]] = relationship(
        "MatchLogORM", foreign_keys="MatchLogORM.team_a_id",
        back_populates="team_a"
    )

    matches_as_team_b: Mapped[List["MatchLogORM"]] = relationship(
        "MatchLogORM", foreign_keys="MatchLogORM.team_b_id",
        back_populates="team_b"
    )

    def __repr__(self):
        return f"<Team(id={self.id}, name={self.name})>"
