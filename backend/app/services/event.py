from sqlalchemy import select
from app.db.engine import AsyncSession
from app.models.event import EventORM
import uuid


async def is_event_existing(event_id: uuid.UUID, session: AsyncSession) -> bool:
    stmt = select(EventORM).where(EventORM.id == event_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
