import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.engine import async_session_maker, engine
from app.db.schema import Base
from app.models.category import CategoryORM
from app.models.player import PlayerORM
from app.models.schemas import Player
from app.models.club import ClubORM
from faker import Faker

fake = Faker()

CATEGORIES = [
    "mens_singles",
    "mens_doubles",
    "womens_singles",
    "womens_doubles",
    "mixed_doubles",
]

fake_tennis_clubs = [
    "The Rochambeau Club",
    "Bushwood Country Club",
    "The Royal Tenenbaum Tennis Center",
    "High Ridge Country Club",
    "Encino Country Club",
    "The Atlanta Tennis Club",
    "Greenbriar Racquet & Country Club",
    "Sunset Ridge Lawn Tennis Club",
    "Pinewood Valley Racquet Club",
    "The Rolling Hills Lawn & Tennis Association",
]


async def _create_category(session: AsyncSession, name: str):
    category_obj = CategoryORM(name=name)
    print(f"Creating: {name}")
    session.add(category_obj)
    await session.flush()
    await session.refresh(category_obj)


async def _create_club(session: AsyncSession, name: str):
    club_obj = ClubORM(name=name)
    print(f"Creating: {name}")
    session.add(club_obj)
    await session.flush()
    await session.refresh(club_obj)


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


async def _seed_players(session: AsyncSession):
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


async def _seed_categories(session: AsyncSession):
    print("Seeding Categories...")
    for category in CATEGORIES:
        await _create_category(session=session, name=category)
    print(f'Successfully added {len(CATEGORIES)} categories.')


async def _seed_clubs(session: AsyncSession):
    print("Seeding Clubs...")
    for club in fake_tennis_clubs:
        await _create_club(session=session, name=club)
    print(f'Successfully added {len(fake_tennis_clubs)} clubs.')


async def _run_seed():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        await _seed_players(session)
        await _seed_clubs(session)
        await _seed_categories(session)
        await session.commit()


def run_seed():
    asyncio.run(_run_seed())
