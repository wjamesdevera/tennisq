from app.db.schema import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Integer, DateTime, func, Table, Column, ForeignKey
from datetime import datetime
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.player import PlayerORM

club_admin = Table(
    "club_admin",
    Base.metadata,
    Column("club_id", ForeignKey("clubs.id"), primary_key=True),
    Column("player_id", ForeignKey("players.id"), primary_key=True),
)

club_player = Table(
    "club_player",
    Base.metadata,
    Column("club_id", ForeignKey("clubs.id"), primary_key=True),
    Column("player_id", ForeignKey("players.id"), primary_key=True),
)


class ClubORM(Base):
    __tablename__ = "clubs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationship
    admins: Mapped[List["PlayerORM"]] = relationship(
        secondary=club_admin,
        back_populates="admin_clubs"
    )

    players: Mapped[List["PlayerORM"]] = relationship(
        secondary=club_player,
        back_populates="clubs"
    )

    def __repr__(self):
        return f"<Club(id={self.id}, name={self.name})>"
