from app.schemas.club import CreateClub
from fastapi import APIRouter, HTTPException, status
from app.core.dependencies import AsyncSessionDep
from app.models.schemas import Club, Event, Player
from app.services.club_service import ClubService

router = APIRouter()


@router.get('')
async def get():
    ...


# GET /v1/api/clubs/:club_id/players
@router.get('/{club_id}/players', status_code=status.HTTP_200_OK)
async def get_club_players(session: AsyncSessionDep, club_id: int):
    club_service = ClubService(session)
    players = await club_service.get_players(club_id)
    return {"status": "success", "result": players}


# POST /v1/api/clubs/:club_id/players
@router.post('/{club_id}/players', status_code=status.HTTP_201_CREATED)
async def create_club_player(player: Player, club_id: int, session: AsyncSessionDep):
    club_service = ClubService(session)
    created_player = await club_service.add_player(player=player, club_id=club_id)
    return {"status": "success", "result": created_player}


# POST /v1/api/clubs/:club_id/events
@router.post('/{club_id}/events', status_code=status.HTTP_201_CREATED)
async def created_event(event: Event, club_id: int, session: AsyncSessionDep):
    club_service = ClubService(session)
    event.club_id = club_id
    created_event = await club_service.add_event(event=event)
    return {"status": "success", "result": created_event}


# POST /v1/api/clubs/
@router.post('', status_code=status.HTTP_201_CREATED)
async def create(club: CreateClub, session: AsyncSessionDep):
    club_service = ClubService(session)
    new_club: Club | None = await club_service.create_club(name=club.name)
    if not new_club:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return {"status": "success", "result": new_club}
