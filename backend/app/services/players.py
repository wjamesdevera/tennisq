import uuid

from app.models.player import PlayerORM
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


async def get_players(session: AsyncSession, skip: int = 0, limit: int = 100):
    stmt = select(PlayerORM).offset(skip).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


async def find_player(player_id: uuid.UUID, session: AsyncSession, with_club: bool = False) -> PlayerORM:
    stmt = select(PlayerORM).where(PlayerORM.id == player_id)
    if with_club:
        stmt = stmt.options(selectinload(PlayerORM.clubs))
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
