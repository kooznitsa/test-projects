from typing import AsyncGenerator, Callable, Generator

import asyncio
import pytest
import pytest_asyncio
from fastapi import FastAPI, Request
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from db.config import settings

test_db = (
    f'postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}'
    f'@{settings.postgres_server}:{settings.postgres_port}/{settings.postgres_db_tests}'
)

engine = create_async_engine(
    test_db,
    echo=settings.db_echo_log,
    future=True,
)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture(scope='session')
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture()
async def db_session() -> AsyncSession:
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.drop_all)
        await connection.run_sync(SQLModel.metadata.create_all)
        async with async_session(bind=connection) as session:
            yield session
            await session.flush()
            await session.rollback()


@pytest.fixture()
def override_get_db(db_session: AsyncSession) -> Callable:
    async def _override_get_db():
        yield db_session

    return _override_get_db


@pytest.fixture()
def app(override_get_db: Callable) -> FastAPI:
    from db.sessions import get_db
    from main import app

    app.dependency_overrides[get_db] = override_get_db

    return app


@pytest_asyncio.fixture()
async def async_client(app: FastAPI) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest_asyncio.fixture()
async def async_client_authenticated(app: FastAPI) -> AsyncGenerator:
    from routers.auth import get_current_user

    def skip_auth():
        pass

    app.dependency_overrides[get_current_user] = skip_auth

    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac
