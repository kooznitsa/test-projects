import asyncio
import asyncpg

from config import settings
import db_queries


async def create_database():
    connection = await asyncpg.connect(
        host=settings.POSTGRES_SERVER,
        port=settings.POSTGRES_PORT,
        user=settings.POSTGRES_USER,
        database=settings.POSTGRES_DB,
        password=settings.POSTGRES_PASSWORD,
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
    print(f'Creating database {settings.POSTGRES_DB}...')
    for statement in statements:
        status = await connection.execute(statement)
        print(status)
    print(f'Database {settings.POSTGRES_DB} has been created.')
    await connection.close()


if __name__ == '__main__':
    asyncio.run(create_database())