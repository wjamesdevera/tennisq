from app.models.player import PlayerORM
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.event import EventORM, event_player
from app.models.player import PlayerORM
from app.schemas.player import ReadPlayer, CreatePlayer
from app.schemas.event import CreateEvent, ReadEvent
from app.core.errors import AlreadyExistsError, NotFoundError
from app.services.player_service import PlayerService
from app.utils import normalize_full_name
import uuid


class EventService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_event(self, event_id: uuid.UUID, with_club: bool = False, with_players: bool = False) -> EventORM | None:
        stmt = select(EventORM).where(EventORM.id == event_id)

        if with_club:
            stmt = stmt.options(joinedload(EventORM.club))
        if with_players:
            stmt = stmt.options(selectinload(EventORM.players))

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_event(self, event_id: uuid.UUID) -> EventORM:
        stmt = select(EventORM).where(EventORM.id == event_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_event_player(self, event_id: uuid.UUID, limit: int = 20, offset: int = 0) -> dict:
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
        players = [ReadPlayer.model_validate(player) for player in players]

        return {
            "limit": limit,
            "offset": offset,
            "total": total,
            "players": players
        }

    async def add_player(self, player: CreatePlayer, event_id: uuid.UUID) -> ReadPlayer:
        # Check if event exist
        event_obj = await self.find_event(event_id, with_players=True)

        # If event does not exist throw not found
        if not event_obj:
            raise NotFoundError(f"Event {event_id} not found.")

        # Check if player exists on event player list
        # If player is player already in the event player list throw  already exist
        new_player_name = normalize_full_name(
            player.first_name, player.last_name)

        event_players = [
            event_player.name for event_player in event_obj.players]

        if new_player_name in event_players:
            raise AlreadyExistsError(
                f"Player {event_player} already exists")
        # else create player
        player_service = PlayerService(self.session)
        new_player = await player_service.create_player(player)
        # add player to the event player list
        event_obj.players.append(new_player)

        formatted_new_player = ReadPlayer.model_validate(new_player)
        return formatted_new_player

    async def create_event(self, event: CreateEvent) -> ReadEvent:
        new_event = EventORM(**event.model_dump())
        self.session.add(new_event)
        await self.session.flush()
        await self.session.refresh(new_event)
        new_event = ReadEvent.model_validate(new_event)
        return new_event
