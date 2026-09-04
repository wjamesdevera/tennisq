# dependencies.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.db.engine import get_async_session, async_session_maker

# Type alias for cleaner dependency injection
AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]


# Alternative: Session with transaction control
async def get_session_with_transaction() -> AsyncSession:
    """
    Provides a session that automatically begins a transaction.
    Useful when you need explicit transaction boundaries.
    """
    async with async_session_maker() as session:
        async with session.begin():
            yield session
