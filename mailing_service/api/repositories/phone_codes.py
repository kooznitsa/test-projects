from typing import Optional

from sqlalchemy import select

from db.errors import EntityDoesNotExist
from repositories.base_repository import BaseRepository
from schemas.phone_codes import PhoneCode, PhoneCodeCreate, PhoneCodeRead, PhoneCodeUpdate


class PhoneCodeRepository(BaseRepository):
    async def _get_instance(self, phone_code_id: int):
        query = select(PhoneCode).where(PhoneCode.id == phone_code_id)
        results = await self.session.exec(query)
        return results.scalars().first()

    async def create(self, phone_code_create: PhoneCodeCreate) -> PhoneCodeRead:
        statement = select(PhoneCode).where(
            PhoneCode.phone_code == phone_code_create.phone_code
        )
        result = await self.session.exec(statement)
        new_phone_code = await self._upsert_value(
            result.scalars().first(), PhoneCode, phone_code_create
        )
        self.session.add(new_phone_code)
        await self.session.commit()
        await self.session.refresh(new_phone_code)
        return new_phone_code

    async def list(self, limit: int, offset: int = 0) -> list[PhoneCodeRead]:
        query = select(PhoneCode).order_by(PhoneCode.id).offset(offset).limit(limit)
        results = await self.session.exec(query)
        return results.scalars().all()

    async def get(self, phone_code_id: int) -> Optional[PhoneCodeRead]:
        if phone_code := await self._get_instance(phone_code_id):
            return phone_code
        else:
            raise EntityDoesNotExist

    async def update(
        self,
        phone_code_id: int,
        phone_code_update: PhoneCodeUpdate,
    ) -> Optional[PhoneCodeRead]:
        if phone_code := await self._get_instance(phone_code_id):
            phone_code_dict = phone_code_update.dict(
                exclude_unset=True,
                exclude={'id'},
            )
            for key, value in phone_code_dict.items():
                setattr(phone_code, key, value)
            self.session.add(phone_code)
            await self.session.commit()
            await self.session.refresh(phone_code)
            return PhoneCodeRead(**phone_code.dict())
        else:
            raise EntityDoesNotExist

    async def delete(self, phone_code_id: int) -> None:
        if phone_code := await self._get_instance(phone_code_id):
            await self.session.delete(phone_code)
            await self.session.commit()
        else:
            raise EntityDoesNotExist
