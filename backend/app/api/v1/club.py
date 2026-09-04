from fastapi import APIRouter, HTTPException, status
from app.core.dependencies import AsyncSessionDep
from app.models.schemas import Club
from app.services.club import create_club
from pydantic import BaseModel

router = APIRouter()


class CreateClub(BaseModel):
    name: str


@router.get('/')
async def get():
    ...


@router.post('', response_model=Club, status_code=status.HTTP_201_CREATED)
async def create(club: CreateClub, session: AsyncSessionDep):
    new_club: Club | None = await create_club(name=club.name, session=session)
    if not new_club:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return new_club.model_dump(mode='json')
