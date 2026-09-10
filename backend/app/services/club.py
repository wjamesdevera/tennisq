from app.models.club import ClubORM
from app.models.event import EventORM
from app.models.player import PlayerORM
from app.models.schemas import Club, Event, Player
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


async def add_player(session: AsyncSession, club_id: int, player: Player):
    stmt = select(ClubORM).where(ClubORM.id == club_id).options(
        selectinload(ClubORM.players))
    result = await session.execute(stmt)
    club_obj = result.scalar_one_or_none()

    player_obj = PlayerORM(**player.model_dump())
    session.add(player_obj)
    await session.flush()
    await session.refresh(player_obj)

    club_obj.players.append(player_obj)
    return player_obj


async def add_event(session: AsyncSession, event: Event):
    event_obj = EventORM(name=event.name, type=event.type,
                         date=event.date, club_id=event.club_id)
    session.add(event_obj)
    await session.flush()
    await session.refresh(event_obj)

    return event_obj
