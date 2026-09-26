import asyncio

from app.models.event import EventORM
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.engine import async_session_maker, engine
from app.db.schema import Base
from app.models.category import CategoryORM
from app.models.player import PlayerORM
from app.schemas.player import Player
from app.schemas.event import Event
from datetime import date, datetime
from faker import Faker

fake = Faker()

CATEGORIES = [
    "mens_singles",
    "mens_doubles",
    "womens_singles",
    "womens_doubles",
    "mixed_doubles",
]


async def _create_category(session: AsyncSession, name: str):
    category_obj = CategoryORM(name=name)
    print(f"Creating: {name}")
    session.add(category_obj)
    await session.flush()
    await session.refresh(category_obj)


def _generate_player() -> Player:
    name = fake.name_nonbinary()
    matches_played = fake.random_int(1, 100)
    games_won = fake.random_int(1, matches_played)
    games_lost = matches_played - games_won
    highest_possible_sets_won = matches_played * 6
    sets_won = (games_won * 6) + fake.random_int(0,
                                                 (highest_possible_sets_won - (games_won * 6)))
    sets_lost = highest_possible_sets_won - (games_won * 6)

    return Player(
        id=None,
        rank=0,
        name=name,
        matches_played=matches_played,
        games_won=games_won,
        games_lost=games_lost,
        sets_won=sets_won,
        sets_lost=sets_lost
    )


def get_random_past_date(years_back: int = 3) -> date:
    return fake.date_between(start_date=f"-{years_back}y", end_date="today")


def _generate_event() -> Event:
    name: str = f'{fake.company()} {fake.catch_phrase()}'
    description: str = f'{fake.text(150)}'
    event_date: date = get_random_past_date()
    return Event(
        id=None,
        name=name,
        description=description,
        max_players=50,
        date=event_date,
        match_logs=[]
    )


async def _seed_events(session: AsyncSession):
    print("Seeding Events...")
    total_players_created = 0

    for event_index in range(50):
        event: Event = _generate_event()
        print(f"Adding: {event.name}")

        event_data = event.model_dump(exclude={"players", "match_logs"})
        event_obj = EventORM(**event_data)
        session.add(event_obj)
        await session.flush()
        await session.refresh(event_obj, attribute_names=["players"])

        number_of_players = fake.random_int(2, 50)
        print(f"Adding {number_of_players} Players to {event_obj.name}...")

        players_for_event: list[PlayerORM] = []
        for _ in range(number_of_players):
            player = _generate_player()
            print(f"Adding: {player.name}")
            player_obj = PlayerORM(
                **player.model_dump(exclude={"id", "created_at", "updated_at"}))
            session.add(player_obj)
            await session.flush()
            await session.refresh(player_obj)

            players_for_event.append(player_obj)
            total_players_created += 1

        event_obj.players = players_for_event

    print(
        f"Successfully added {total_players_created} players across 50 events.")
    print("Successfully added 50 events.")


async def _seed_players(session: AsyncSession):
    print("Seeding Players...")

    for i in range(1000):
        player = _generate_player()
        player.rank = i + 1
        print(f"Adding: {player.name}")
        player_obj = PlayerORM(
            **player.model_dump(exclude={"id", "created_at", "updated_at"}))
        session.add(player_obj)
        await session.flush()
        await session.refresh(player_obj)
    print(f"Successfully added {1000} players.")


async def _seed_categories(session: AsyncSession):
    print("Seeding Categories...")
    for category in CATEGORIES:
        await _create_category(session=session, name=category)
    print(f'Successfully added {len(CATEGORIES)} categories.')


async def reset_schema(engine):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)


async def run_seed(session):
    """Seed data using an existing session. Awaitable directly from async code."""
    await _seed_categories(session)
    await session.commit()


def run_seed_cli():
    """Sync entrypoint for CLI/script usage — builds its own engine/session."""
    async def _main():
        await reset_schema(engine)
        async with async_session_maker() as session:
            await run_seed(session)

    asyncio.run(_main())
