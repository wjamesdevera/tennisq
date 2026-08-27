from sqlalchemy.orm import mapped_column, Mapped
from app.db.schema import Base
from sqlalchemy import String, Integer, DateTime, func, UUID
from datetime import datetime
import uuid


class PlayerModel(Base):
    __tablename__ = "players"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    name: Mapped[str] = mapped_column(String(200))
    rank: Mapped[int] = mapped_column(Integer())
    games_won: Mapped[int] = mapped_column(Integer())
    games_lost: Mapped[int] = mapped_column(Integer())
    sets_won: Mapped[int] = mapped_column(Integer())
    sets_lost: Mapped[int] = mapped_column(Integer())
    matches_played: Mapped[int] = mapped_column(Integer())

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return f"<Player(id={self.id}, name={self.name})>"
