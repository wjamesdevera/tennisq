from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import func, DateTime
from datetime import datetime, timezone
from typing import Optional
import uuid


class Base(DeclarativeBase):
    pass

# class EventTimestampModel(Base):
#     occured_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True), server_default=func.now()
#     )
