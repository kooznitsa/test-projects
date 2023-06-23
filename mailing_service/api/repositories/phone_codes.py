from typing import Optional

from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.errors import EntityDoesNotExist
from repositories.base_methods import upsert_value
from schemas.phone_codes import PhoneCode, PhoneCodeCreate, PhoneCodeRead


class PhoneCodeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, phone_code_create: PhoneCodeCreate) -> PhoneCodeRead:
        statement = select(PhoneCode).where(PhoneCode.phone_code == phone_code_create.phone_code)
        result = await self.session.exec(statement)

        return await upsert_value(
            self.session,
            result.scalars().first(),
            PhoneCode.from_orm(phone_code_create)
        )

    async def _get_instance(self, phone_code_id: int):
        query = (
            select(PhoneCode)
            .where(PhoneCode.id == phone_code_id)
        )
        results = await self.session.exec(query)

        return results.scalars().first()

    async def list(
        self,
        limit: int = 10,
        offset: int = 0,
    ) -> list[PhoneCodeRead]:
        query = select(PhoneCode).order_by(PhoneCode.id).offset(offset).limit(limit)
        results = await self.session.exec(query)
        return results.scalars().all()

    async def get(self, phone_code_id: int) -> Optional[PhoneCodeRead]:
        if phone_code := await self._get_instance(phone_code_id):
            return phone_code
        else:
            raise EntityDoesNotExist
