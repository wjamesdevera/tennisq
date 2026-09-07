from fastapi import APIRouter, status
from app.core.dependencies import AsyncSessionDep
from app.services.players import get_players, get_players_from_club

router = APIRouter()


@router.get('', status_code=status.HTTP_200_OK)
async def get(session: AsyncSessionDep):
    players = await get_players(session=session, skip=10, limit=20)
    return {"success": "ok", "result": players}
