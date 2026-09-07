from fastapi import APIRouter, HTTPException, status
from app.core.dependencies import AsyncSessionDep
from app.models.schemas import Club
from app.services.club import create_club, get_players
from pydantic import BaseModel

router = APIRouter()


class CreateClub(BaseModel):
    name: str


@router.get('')
async def get():
    ...


@router.get('/{club_id}/players', status_code=status.HTTP_200_OK)
async def get_club_players(session: AsyncSessionDep, club_id: int):
    players = await get_players(session=session, club_id=club_id)
    return {"success": "ok", "result": players}


@router.post('', response_model=Club, status_code=status.HTTP_201_CREATED)
async def create(club: CreateClub, session: AsyncSessionDep):
    new_club: Club | None = await create_club(name=club.name, session=session)
    if not new_club:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return new_club.model_dump(mode='json')
