from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db.errors import EntityDoesNotExist
from repositories.base import BaseRepository
from schemas.phone_codes import PhoneCode, PhoneCodeCreate, PhoneCodeRead, PhoneCodeUpdate


class PhoneCodeRepository(BaseRepository):
    model = PhoneCode

    async def create(
        self,
        model_create: PhoneCodeCreate,
        parent_model=None,
        model_id=None,
    ) -> PhoneCodeRead:
        phone_code_query = (
            select(self.model)
            .where(self.model.phone_code == model_create.phone_code)
        )
        result = await self._upsert(phone_code_query, self.model, model_create)
        self.session.add(result)

        if parent_model:
            model_query = await self.session.scalars(
                select(parent_model)
                .where(parent_model.id == model_id)
                .options(selectinload(parent_model.phone_codes))
            )
            if item := model_query.first():
                item.phone_codes.append(result)
            else:
                raise EntityDoesNotExist

        await self.session.commit()
        await self.session.refresh(result)
        return result

    async def list(self, limit: int, offset: int = 0) -> list[PhoneCodeRead]:
        return await super().list(self.model, limit, offset)

    async def get(self, model_id: int) -> Optional[PhoneCodeRead]:
        return await super().get(self.model, model_id)

    async def update(self, model_id: int, model_update: PhoneCodeUpdate) -> Optional[PhoneCodeRead]:
        return await super().update(self.model, model_id, model_update)
