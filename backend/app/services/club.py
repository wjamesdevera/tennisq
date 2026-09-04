
from app.models.club import ClubORM
from app.models.schemas import Club
from sqlalchemy.ext.asyncio import AsyncSession


async def create_club(name: str, session: AsyncSession) -> Club:
    club_obj = ClubORM(name=name)
    session.add(club_obj)
    await session.flush()
    await session.refresh(club_obj, attribute_names=['admins', 'players'])
    return Club.model_validate(club_obj)
