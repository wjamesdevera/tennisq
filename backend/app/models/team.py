from app.db.schema import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Integer, DateTime, func
from datetime import datetime
from pydantic import BaseModel


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

    def __repr__(self):
        return f"<Team(id={self.id}, name={self.name})>"


class Team(BaseModel):
    id: int
    name: str
    created_at: datetime | None
    updated_at: datetime | None
