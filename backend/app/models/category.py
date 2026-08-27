from app.db.schema import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Integer, DateTime, func
from datetime import datetime
from app.models.schemas import Category
from typing import List

from app.models.match import MatchLogORM


class CategoryORM(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    match_logs: Mapped[List["MatchLogORM"]] = relationship(
        "MatchLogORM", back_populates="category"
    )

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name})>"
