from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import func, DateTime
from datetime import datetime, timezone
from typing import Optional
import uuid


class Base(DeclarativeBase):
    pass


class SimpleIDModel(Base):
    id: Mapped[int] = mapped_column(primary_key=True)


class UUIDModel(Base):
    id: Mapped[uuid.UUID] = mapped_column(
        default_factory=uuid.uuid4, primary_key=True)


class TimestampModel(Base):
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class EventTimestampModel(Base):
    occured_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
