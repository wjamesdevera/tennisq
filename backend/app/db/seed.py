import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.engine import async_session_maker, engine
from app.db.schema import Base
from app.models.category import CategoryORM
from app.models.player import PlayerORM
from app.models.schemas import Player
from faker import Faker

fake = Faker()

CATEGORIES = [
    "mens_singles",
    "mens_doubles",
    "womens_singles",
    "womens_doubles",
    "mixed_doubles",
]


async def seed_categories(session: AsyncSession):
    print("Seeding Categories...")
    for category in CATEGORIES:
        print(f"Adding: {category}")
        category_obj = CategoryORM(name=category)
        session.add(category_obj)
        await session.flush()
        await session.refresh(category_obj)
    print(f'Successfully added {len(CATEGORIES)} categories.')


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
        name=name,
        matches_played=matches_played,
        games_won=games_won,
        games_lost=games_lost,
        sets_won=sets_won,
        sets_lost=sets_lost
    )


async def seed_players(session: AsyncSession):
    print("Seeding Players...")

    for i in range(1000):
        player = _generate_player()
        print(f"Adding: {player.name}")
        player.rank = i + 1
        player_obj = PlayerORM(**player.model_dump())
        session.add(player_obj)
        await session.flush()
        await session.refresh(player_obj)
    print(f'Successfully added {1000} players.')


async def _run_seed():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        await seed_players(session)
        await seed_categories(session)
        await session.commit()


def run_seed():
    asyncio.run(_run_seed())
