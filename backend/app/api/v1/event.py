import uuid

from app.schemas.player import CreatePlayer
from fastapi import APIRouter, status, HTTPException
from app.core.dependencies import AsyncSessionDep
from app.services.event_service import EventService
from app.schemas.event import CreateEvent, ReadEvent
from app.core.errors import NotFoundError, AlreadyExistsError

router = APIRouter()


# GET /v1/events/:event_id
@router.get('/{event_id}', status_code=status.HTTP_200_OK)
async def get_event(event_id: uuid.UUID, session: AsyncSessionDep):
    event_service = EventService(session)
    event = await event_service.get_event(event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status": "error",
                "message": f"Event ID: {event_id} not found",
                "code": 404,
            }
        )
    formatted_event = ReadEvent.model_validate(event)
    return {
        "status": "success",
        "data": formatted_event,
    }


# GET /v1/events/:event_id/players
@router.get('/{event_id}/players', status_code=status.HTTP_200_OK)
async def get_event_players(event_id: uuid.UUID, session: AsyncSessionDep, limit: int = 20, offset: int = 0):
    event_service = EventService(session)
    try:
        players = await event_service.get_event_player(event_id, limit, offset)
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status": "error",
                "message": f"Event ID: {event_id} not found",
                "code": 404,
            }
        )

    return {
        "status": "success",
        "data": players,
    }


# POST /v1/events/
@router.post('', status_code=status.HTTP_201_CREATED)
async def create_event(event: CreateEvent, session: AsyncSessionDep):
    event_service = EventService(session)
    new_event = await event_service.create_event(event)
    return {
        "status": "success",
        "data": new_event
    }


# POST /v1/events/:event_id/players
@router.post('/{event_id}/players', status_code=status.HTTP_201_CREATED)
async def add_player(event_id: uuid.UUID, player: CreatePlayer, session: AsyncSessionDep):
    event_service = EventService(session)
    try:
        new_player = await event_service.add_player(player=player, event_id=event_id)
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status": "error",
                "message": f"Event ID: {event_id} not found.",
                "code": 404,
            }
        )
    except AlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "status": "error",
                "message": f"Player: {player.first_name} {player.last_name} already exist.",
                "code": 409,
            }
        )

    return {
        "status": "success",
        "data": new_player
    }
