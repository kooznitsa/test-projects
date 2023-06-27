from typing import Optional

from sqlalchemy import select

from db.errors import EntityDoesNotExist
from repositories.base_repository import BaseRepository
from schemas.timezones import Timezone, TimezoneCreate, TimezoneRead, TimezoneUpdate


class TimezoneRepository(BaseRepository):
    async def create(self, timezone_create: TimezoneCreate) -> TimezoneRead:
        statement = select(Timezone).where(Timezone.timezone == timezone_create.timezone)
        result = await self.session.exec(statement)
        new_timezone = await self._upsert_value(result.scalars().first(), Timezone, timezone_create)
        self.session.add(new_timezone)
        await self.session.commit()
        await self.session.refresh(new_timezone)
        return new_timezone

    async def _get_instance(self, timezone_id: int):
        query = (select(Timezone).where(Timezone.id == timezone_id))
        results = await self.session.exec(query)
        return results.scalars().first()

    async def list(self, limit: int, offset: int = 0) -> list[TimezoneRead]:
        query = select(Timezone).order_by(Timezone.id).offset(offset).limit(limit)
        results = await self.session.exec(query)
        return results.scalars().all()

    async def get(self, timezone_id: int) -> Optional[TimezoneRead]:
        if timezone := await self._get_instance(timezone_id):
            return timezone
        else:
            raise EntityDoesNotExist

    async def update(
        self,
        timezone_id: int,
        timezone_update: TimezoneUpdate,
    ) -> Optional[TimezoneRead]:
        if timezone := await self._get_instance(timezone_id):
            timezone_dict = timezone_update.dict(
                exclude_unset=True,
                exclude={'id'},
            )
            for key, value in timezone_dict.items():
                setattr(timezone, key, value)
            self.session.add(timezone)
            await self.session.commit()
            await self.session.refresh(timezone)
            return TimezoneRead(**timezone.dict())
        else:
            raise EntityDoesNotExist

    async def delete(self, timezone_id: int) -> None:
        if timezone := await self._get_instance(timezone_id):
            await self.session.delete(timezone)
            await self.session.commit()
        else:
            raise EntityDoesNotExist
