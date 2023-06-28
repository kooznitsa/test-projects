from typing import Optional

from sqlalchemy import select

from repositories.base import BaseRepository
from schemas.timezones import Timezone, TimezoneCreate, TimezoneRead, TimezoneUpdate


class TimezoneRepository(BaseRepository):
    model = Timezone
    model_read = TimezoneRead

    async def create(self, model_create: TimezoneCreate) -> TimezoneRead:
        query = select(self.model).where(self.model.timezone == model_create.timezone)
        return await super().create(query, self.model, model_create)

    async def list(self, limit: int, offset: int = 0) -> list[TimezoneRead]:
        return await super().list(self.model, limit, offset)

    async def get(self, model_id: int) -> Optional[TimezoneRead]:
        return await super().get(self.model, model_id)

    async def update(self, model_id: int, model_update: TimezoneUpdate) -> Optional[TimezoneRead]:
        return await super().update(self.model, model_id, model_update, self.model_read)
