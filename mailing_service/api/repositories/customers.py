from typing import Optional

from sqlalchemy.orm import selectinload
from sqlmodel import select

from db.errors import EntityDoesNotExist, PhoneLengthError
from repositories.base import BaseRepository
from schemas.phone_codes import PhoneCode, PhoneCodeCreate, PhoneCodeRead
from schemas.timezones import Timezone, TimezoneCreate, TimezoneRead
from schemas.tags import Tag, TagCreate, TagRead
from schemas.customers import Customer, CustomerCreate, CustomerRead, CustomerUpdate


class CustomerRepository(BaseRepository):
    model = Customer

    async def create(self, model_create: CustomerCreate) -> CustomerRead:
        phone_code_query = await self.session.exec(
            select(PhoneCode)
            .where(PhoneCode.id == model_create.phone_code_id)
        )
        phone_code = phone_code_query.first()
        timezone_query = await self.session.exec(
            select(Timezone)
            .where(Timezone.id == model_create.timezone_id)
        )
        timezone = timezone_query.first()

        if len(str(model_create.phone)) != 7:
            raise PhoneLengthError
        if not phone_code or not timezone:
            raise EntityDoesNotExist
        else:
            return await self._create_not_unique(self.model, model_create)

    async def list(
        self,
        limit: int,
        tag: Optional[str] = None,
        phone_code: int | None = None,
        offset: int = 0,
    ) -> list[CustomerRead]:
        query = select(self.model).order_by(self.model.id)
        if tag:
            query = query.where(self.model.tags.any(Tag.tag == tag))
        if phone_code:
            query = (
                query.join(PhoneCode)
                .where(PhoneCode.id == self.model.phone_code_id)
                .where(PhoneCode.phone_code == phone_code)
            )
        query = query.offset(offset).limit(limit)

        results = await self.session.exec(
            query.options(selectinload(self.model.tags))
        )
        return results.all()

    async def get(self, model_id: int) -> Optional[CustomerRead]:
        return await super().get(self.model, model_id)

    async def update(self, model_id: int, model_update: CustomerUpdate) -> Optional[CustomerRead]:
        if len(str(model_update.phone)) != 7:
            raise PhoneLengthError
        return await super().update(self.model, model_id, model_update)

    async def delete_customer_tag(self, model_id: int, tag_id: int) -> Optional[CustomerRead]:
        return await super().delete_model_tag(self.model, model_id, Tag, tag_id)
