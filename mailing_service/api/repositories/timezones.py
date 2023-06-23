from typing import Optional

from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.errors import EntityDoesNotExist
from repositories.base_methods import upsert_value
from schemas.timezones import Timezone, TimezoneCreate, TimezoneRead


class TimezoneRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, timezone_create: TimezoneCreate) -> TimezoneRead:
        statement = select(Timezone).where(Timezone.timezone == timezone_create.timezone)
        result = await self.session.exec(statement)

        return await upsert_value(
            self.session,
            result.scalars().first(),
            Timezone.from_orm(timezone_create)
        )

    async def _get_instance(self, timezone_id: int):
        query = (
            select(Timezone)
            .where(Timezone.id == timezone_id)
        )
        results = await self.session.exec(query)

        return results.scalars().first()

    async def list(
        self,
        limit: int = 10,
        offset: int = 0,
    ) -> list[TimezoneRead]:
        query = select(Timezone).order_by(Timezone.id).offset(offset).limit(limit)
        results = await self.session.exec(query)
        return results.scalars().all()

    async def get(self, timezone_id: int) -> Optional[TimezoneRead]:
        if timezone := await self._get_instance(timezone_id):
            return timezone
        else:
            raise EntityDoesNotExist
