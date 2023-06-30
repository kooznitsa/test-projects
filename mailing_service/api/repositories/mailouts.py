from typing import Optional

from sqlalchemy.orm import selectinload
from sqlmodel import select

from db.errors import EntityDoesNotExist
from repositories.base import BaseRepository
from schemas.phone_codes import PhoneCode
from schemas.tags import Tag
from schemas.mailouts import Mailout, MailoutRead, MailoutCreate, MailoutUpdate


class MailoutRepository(BaseRepository):
    model = Mailout
    model_read = MailoutRead

    async def create(self, model_create: MailoutCreate) -> MailoutRead:
        return await self._create_not_unique(self.model, model_create)

    async def list(
        self,
        limit: int,
        tag: Optional[str] = None,
        phone_code: int | None = None,
        offset: int = 0,
    ) -> list[MailoutRead]:
        query = select(self.model).order_by(self.model.id)
        if tag:
            query = query.where(self.model.tags.any(Tag.tag == tag))
        if phone_code:
            query = query.where(self.model.phone_codes.any(PhoneCode.phone_code == phone_code))
        query = query.offset(offset).limit(limit)
        results = await self.session.exec(query.options(selectinload('*')))
        return results.all()

    async def get(self, model_id: int) -> Optional[MailoutRead]:
        if mailout := await self._get_instance(self.model, model_id):
            return await self._get_instance_with_related(self.model, mailout)
        else:
            raise EntityDoesNotExist

    async def update(self, model_id: int, model_update: MailoutUpdate) -> Optional[MailoutRead]:
        item = await super().update(self.model, model_id, model_update, self.model_read)
        return await self._get_instance_with_related(self.model, item)

    async def delete_mailout_tag(
        self,
        mailout_id: int,
        tag_id: int,
    ) -> Optional[MailoutRead]:

        tag_query = await self.session.scalars(select(Tag).where(Tag.id == tag_id))
        tag_to_delete = tag_query.first()

        mailout_query = select(self.model).where(self.model.id == mailout_id)
        mailout = await self.session.scalars(mailout_query.options(selectinload('*')))

        if mailout := mailout.first():
            mailout.tags.remove(tag_to_delete)
            await self._add_to_db(mailout)
            return await self._get_instance_with_related(self.model, mailout)
        else:
            raise EntityDoesNotExist

    async def delete_mailout_phone_code(
        self,
        mailout_id: int,
        phone_code_id: int,
    ) -> Optional[MailoutRead]:

        phone_code_query = await self.session.scalars(select(PhoneCode).where(PhoneCode.id == phone_code_id))
        phone_code_to_delete = phone_code_query.first()

        mailout_query = select(self.model).where(self.model.id == mailout_id)
        mailout = await self.session.scalars(mailout_query.options(selectinload('*')))

        if mailout := mailout.first():
            mailout.phone_codes.remove(phone_code_to_delete)
            await self._add_to_db(mailout)
            return await self._get_instance_with_related(self.model, mailout)
        else:
            raise EntityDoesNotExist
