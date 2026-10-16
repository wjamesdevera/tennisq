import uuid

from app.models.player import PlayerORM
from app.schemas.player import CreatePlayer, ReadPlayer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.core.errors import AlreadyExistsError
from app.utils import normalize_full_name


class PlayerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_player_by_id(self, player_id: uuid.UUID, with_club: bool = False) -> PlayerORM:

        stmt = select(PlayerORM).where(PlayerORM.id == player_id)
        if with_club:
            stmt = stmt.options(selectinload(PlayerORM.clubs))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_player_by_name(self, name: str) -> PlayerORM:
        stmt = select(PlayerORM).where(PlayerORM.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_player(self, create_player: CreatePlayer) -> PlayerORM:
        player_name = normalize_full_name(
            create_player.first_name, create_player.last_name)

        new_player = PlayerORM(
            name=player_name,
        )
        self.session.add(new_player)
        await self.session.flush()
        await self.session.refresh(new_player)
        return new_player
