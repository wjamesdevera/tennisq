from app.models.player import PlayerORM
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_players(session: AsyncSession, skip: int = 0, limit: int = 100):
    stmt = select(PlayerORM).offset(skip).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()
