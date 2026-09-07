
from app.models.club import ClubORM
from app.models.schemas import Club
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload


async def create_club(name: str, session: AsyncSession) -> Club:
    club_obj = ClubORM(name=name)
    session.add(club_obj)
    await session.flush()
    await session.refresh(club_obj, attribute_names=['admins', 'players'])
    return Club.model_validate(club_obj)


async def get_players(session: AsyncSession, club_id: int):
    stmt = select(ClubORM).options(
        selectinload(ClubORM.players)).where(ClubORM.id == club_id)
    result = await session.execute(stmt)
    club_obj = result.scalar_one_or_none()
    return club_obj.players
