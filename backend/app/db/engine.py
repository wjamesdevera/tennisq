from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)
from app.core.config import config
from typing import AsyncGenerator

engine = create_async_engine(
    config.db_url,
    echo=config.debug,  # Set to False in production
    pool_size=5,  # Number of connections to keep open
    max_overflow=10,  # Additional connections when pool is exhausted
    pool_timeout=30,  # Seconds to wait for a connection
    pool_recycle=1800,  # Recycle connections after 30 minutes
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Prevent lazy loading issues after commit
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides an async database session.
    Automatically handles commit/rollback and session cleanup.
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
