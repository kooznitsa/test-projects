from typing import Generator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from db.config import settings

engine = create_engine(
    url=settings.sync_database_url,
    echo=settings.db_echo_log,
)

async_engine = create_async_engine(
    url=settings.async_database_url,
    echo=settings.db_echo_log,
    future=True,
)

async_session = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


def get_session() -> Generator:
    with Session(engine) as session:
        yield session


def get_async_session() -> Generator:
    with AsyncSession(engine) as async_session:
        yield async_session


def create_tables_from_models():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)