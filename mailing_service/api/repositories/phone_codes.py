from typing import Optional

from sqlalchemy import select

from repositories.base import BaseRepository
from schemas.phone_codes import PhoneCode, PhoneCodeCreate, PhoneCodeRead, PhoneCodeUpdate


class PhoneCodeRepository(BaseRepository):
    model = PhoneCode
    model_read = PhoneCodeRead

    async def create(self, model_create: PhoneCodeCreate) -> PhoneCodeRead:
        query = select(self.model).where(self.model.phone_code == model_create.phone_code)
        return await super().create(query, self.model, model_create)

    async def list(self, limit: int, offset: int = 0) -> list[PhoneCodeRead]:
        return await super().list(self.model, limit, offset)

    async def get(self, model_id: int) -> Optional[PhoneCodeRead]:
        return await super().get(self.model, model_id)

    async def update(self, model_id: int, model_update: PhoneCodeUpdate) -> Optional[PhoneCodeRead]:
        return await super().update(self.model, model_id, model_update, self.model_read)
