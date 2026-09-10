# dependencies.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.db.engine import get_async_session

# Type alias for cleaner dependency injection
AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
