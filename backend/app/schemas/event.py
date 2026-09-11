from pydantic import BaseModel
from datetime import datetime


class CreateEvent(BaseModel):
    name: str
    type: str
    date: str = datetime.now().date()
    club_id: int = None
