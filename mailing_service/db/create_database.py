import asyncio
import asyncpg

from db.config import settings
from db import db_queries
from db.sessions import async_session, async_system_session


async def create_db_if_not_exists():
    """Creates the database if it doesn't exist and connects to it."""
    database = settings.postgres_db
    user = settings.postgres_user

    try:
        session = async_session()
        print(f'Connection to the database {database} established.')
    except asyncpg.InvalidCatalogNameError:
        session = async_system_session()
        await session.execute(
            f'CREATE DATABASE "{database}" OWNER "{user}"'
        )
        print(f'Database {database} has been created.')
        await session.close()

    return session


async def create_tables():
    """Creates tables in the database."""
    session = asyncio.get_event_loop().run_until_complete(
        await create_db_if_not_exists()
    )

    statements = [
        db_queries.CREATE_STATUSES,
        db_queries.CREATE_TIMEZONES,
        db_queries.CREATE_PHONE_CODES,
        db_queries.CREATE_TAGS,
        db_queries.CREATE_MAILOUTS,
        db_queries.CREATE_CUSTOMERS,
        db_queries.CREATE_MESSAGES,
        db_queries.CREATE_MAILOUTS_CUSTOMERS,
        db_queries.CREATE_MAILOUTS_PHONE_CODES,
        db_queries.CREATE_MAILOUTS_TAGS,
        db_queries.CREATE_CUSTOMERS_TAGS,
    ]
    print(f'Creating tables in the database {settings.postgres_db}...')
    for statement in statements:
        status = await session.execute(statement)
        print(status)
    print(f'Tables in the database {settings.postgres_db} have been created.')
    await session.close()


if __name__ == '__main__':
    asyncio.run(create_tables())