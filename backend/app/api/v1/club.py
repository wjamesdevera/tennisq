from fastapi import APIRouter, HTTPException, status
from app.core.dependencies import AsyncSessionDep
from app.models.schemas import Club, Player
from app.services.club import add_player, create_club, get_players
from pydantic import BaseModel

router = APIRouter()


class CreateClub(BaseModel):
    name: str


@router.get('')
async def get():
    ...


# GET /v1/api/clubs/:club_id/players
@router.get('/{club_id}/players', status_code=status.HTTP_200_OK)
async def get_club_players(session: AsyncSessionDep, club_id: int):
    players = await get_players(session=session, club_id=club_id)
    return {"success": "ok", "result": players}


# POST /v1/api/clubs/:club_id/players
@router.post('/{club_id}/players', status_code=status.HTTP_201_CREATED)
async def create_club_player(player: Player, club_id: int, session: AsyncSessionDep):
    created_player = await add_player(session=session, player=player, club_id=club_id)
    return {"success": "ok", "result": created_player}


# POST /v1/api/clubs/
@router.post('', response_model=Club, status_code=status.HTTP_201_CREATED)
async def create(club: CreateClub, session: AsyncSessionDep):
    new_club: Club | None = await create_club(name=club.name, session=session)
    if not new_club:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return new_club.model_dump(mode='json')
