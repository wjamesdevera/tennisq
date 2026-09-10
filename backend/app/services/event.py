from app.models.player import PlayerORM
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from app.db.engine import AsyncSession
from app.models.event import EventORM
import uuid


async def find_event(event_id: uuid.UUID, session: AsyncSession) -> EventORM:
    stmt = select(EventORM).where(
        EventORM.id == event_id).options(joinedload(EventORM.club))
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def add_player(player_id: uuid.UUID, event_id: uuid.UUID, session: AsyncSession) -> EventORM:
    stmt = select(EventORM).where(
        EventORM.id == event_id).options(selectinload(EventORM.players))
    result = await session.execute(stmt)
    event_obj = result.scalar_one_or_none()
    stmt = select(PlayerORM).where(
        PlayerORM.id == player_id)
    result = await session.execute(stmt)
    player_obj = result.scalar_one_or_none()

    event_obj.players.append(player_obj)
    return event_obj
