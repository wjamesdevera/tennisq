from app.models.player import PlayerORM
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.event import EventORM, event_player
from app.models.player import PlayerORM
from app.schemas.event import CreateEvent, ReadEvent
from app.core.errors import NotFoundError
from typing import List
import uuid


class EventService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_event(self, event_id: uuid.UUID) -> EventORM:
        stmt = select(EventORM).where(
            EventORM.id == event_id).options(joinedload(EventORM.club))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_event(self, event_id: uuid.UUID) -> EventORM:
        stmt = select(EventORM).where(EventORM.id == event_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_event_player(self, event_id: uuid.UUID, limit: int = 20, offset: int = 0) -> List[PlayerORM]:
        # 1. Make sure the event exists (so "no players" != "no such event")
        event_exists = await self.session.scalar(
            select(EventORM.id).where(EventORM.id == event_id)
        )
        if event_exists is None:
            raise NotFoundError(f"Event {event_id} not found.")

        # 2. Total count, without loading any players
        total = await self.session.scalar(
            select(func.count())
            .select_from(event_player)
            .where(event_player.c.event_id == event_id)
        )

        stmt = (
            select(PlayerORM)
            .join(event_player, event_player.c.player_id == PlayerORM.id)
            .where(event_player.c.event_id == event_id)
            .order_by(PlayerORM.name, PlayerORM.id)
            .limit(limit)
            .offset(offset)
        )
        players = (await self.session.scalars(stmt)).all()

        return {
            "limit": limit,
            "offset": offset,
            "total": total,
            "players": players
        }

    async def add_player(self, player_id: uuid.UUID, event_id: uuid.UUID) -> EventORM:
        stmt = select(EventORM).where(
            EventORM.id == event_id).options(selectinload(EventORM.players))
        result = await self.session.execute(stmt)
        event_obj = result.scalar_one_or_none()
        stmt = select(PlayerORM).where(
            PlayerORM.id == player_id)
        result = await self.session.execute(stmt)
        player_obj = result.scalar_one_or_none()

        event_obj.players.append(player_obj)
        return event_obj

    async def create_event(self, event: CreateEvent) -> ReadEvent:
        new_event = EventORM(**event.model_dump())
        self.session.add(new_event)
        await self.session.flush()
        await self.session.refresh(new_event)
        new_event = ReadEvent.model_validate(new_event)
        return new_event
