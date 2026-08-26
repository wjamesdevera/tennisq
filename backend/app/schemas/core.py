from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from datetime import datetime, timezone
from typing import Optional
import uuid


class BaseModel(DeclarativeBase):
    pass


class SimpleIDModel(BaseModel):
    id: int = mapped_column(primary_key=True)


class UUIDModel(BaseModel):
    id: uuid.UUID = mapped_column(default_factory=uuid.uuid4, primary_key=True)


class TimestampModel(BaseModel):
    created_at: Optional[datetime] = mapped_column(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: Optional[datetime] = mapped_column(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={
            "onupdate": lambda:
                datetime.now(timezone.utc)
        }
    )


class EventTimestampModel(BaseModel):
    occured_at: Optional[datetime] = mapped_column(
        default_factory=lambda: datetime.now(timezone.utc)

    )
