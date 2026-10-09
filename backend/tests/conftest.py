from datetime import date

import pytest_asyncio
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from app.db.engine import get_async_session
from app.main import app
from app.core.config import config
from app.db.seed import reset_schema
from app.models.event import EventORM


@pytest_asyncio.fixture(name="session")
async def session_fixture():
    engine = create_async_engine(
        config.test_db_url,
        echo=config.debug,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800,
    )

    async_session_maker = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    await reset_schema(engine)

    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    await engine.dispose()


@pytest_asyncio.fixture(name="client")
async def client_fixture(session: AsyncSession):
    def get_session_override():
        return session

    app.dependency_overrides[get_async_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(name="event")
async def event_fixture(session: AsyncSession) -> EventORM:
    event = EventORM(
        name="Test Event",
        description="Event used to test retrieving an event",
        date=date(2026, 9, 26),
        max_players=30,
    )
    session.add(event)
    await session.flush()
    await session.refresh(event)
    return event
