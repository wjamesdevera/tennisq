import uuid

from app.services.players import find_player
from fastapi import APIRouter, status, HTTPException
from app.core.dependencies import AsyncSessionDep
from app.services.event import EventService
from pydantic import BaseModel

router = APIRouter()


class PlayerIdModel(BaseModel):
    id: uuid.UUID


# PATCH /events/:event_id/players
@router.patch('/{event_id}/players', status_code=status.HTTP_200_OK)
async def add_player(event_id: uuid.UUID, player: PlayerIdModel, session: AsyncSessionDep):
    event_service = EventService(session)
    event_obj = await event_service.find_event(event_id)
    if not event_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status": "error",
                "message": f"Event ID: {event_id} not found",
                "code": 404,
            }
        )
    player_obj = await find_player(player.id, session, with_club=True)
    if not player_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status": "error",
                "message": f"Player ID: {player.id} not found",
                "code": 404,
            }
        )
    if event_obj.club not in player_obj.clubs:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "error",
                "message": f"{player_obj.name} not member of club {event_obj.club.name}",
                "code": 400,
            }
        )

    updated_event = await event_service.add_player(player_obj.id, event_obj.id, session)

    # if member is part of club add player to event
    return {"success": "ok", "result": updated_event}
