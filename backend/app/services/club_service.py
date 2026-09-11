from asyncio import Event

from app.models.club import ClubORM
from app.models.event import EventORM
from app.models.player import PlayerORM
from app.schemas.club import Club
from app.schemas.player import Player
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload


class ClubService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_club(self, name: str, ) -> Club:
        club_obj = ClubORM(name=name)
        self.session.add(club_obj)
        await self.session.flush()
        await self.session.refresh(club_obj, attribute_names=['admins', 'players'])
        return Club.model_validate(club_obj)

    async def get_players(self, club_id: int):
        stmt = select(ClubORM).options(
            selectinload(ClubORM.players)).where(ClubORM.id == club_id)
        result = await self.session.execute(stmt)
        club_obj = result.scalar_one_or_none()
        return club_obj.players

    async def add_player(self, club_id: int, player: Player):
        stmt = select(ClubORM).where(ClubORM.id == club_id).options(
            selectinload(ClubORM.players))
        result = await self.session.execute(stmt)
        club_obj = result.scalar_one_or_none()

        player_obj = PlayerORM(**player.model_dump())
        self.session.add(player_obj)
        await self.session.flush()
        await self.session.refresh(player_obj)

        club_obj.players.append(player_obj)
        return player_obj

    async def add_event(self, event: Event):
        event_obj = EventORM(name=event.name, type=event.type,
                             date=event.date, club_id=event.club_id)
        self.session.add(event_obj)
        await self.session.flush()
        await self.session.refresh(event_obj)

        return event_obj
