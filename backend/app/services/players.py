import uuid

from app.models.player import PlayerORM
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class PlayerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_player(self, player_id: uuid.UUID, with_club: bool = False) -> PlayerORM:

        stmt = select(PlayerORM).where(PlayerORM.id == player_id)
        if with_club:
            stmt = stmt.options(selectinload(PlayerORM.clubs))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
