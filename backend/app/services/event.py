from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.db.engine import AsyncSession
from app.models.event import EventORM
import uuid


async def find_event(event_id: uuid.UUID, session: AsyncSession) -> EventORM:
    stmt = select(EventORM).where(
        EventORM.id == event_id).options(joinedload(EventORM.club))
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
