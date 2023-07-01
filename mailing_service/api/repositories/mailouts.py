from typing import Optional

from sqlalchemy.orm import selectinload
from sqlmodel import select

from repositories.base import BaseRepository
from schemas.phone_codes import PhoneCode
from schemas.tags import Tag
from schemas.mailouts import Mailout, MailoutRead, MailoutCreate, MailoutUpdate


class MailoutRepository(BaseRepository):
    model = Mailout

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
        return await super().get(self.model, model_id)

    async def update(self, model_id: int, model_update: MailoutUpdate) -> Optional[MailoutRead]:
        return await super().update(self.model, model_id, model_update)

    async def delete_mailout_tag(self, model_id: int, tag_id: int) -> Optional[MailoutRead]:
        return await super().delete_model_tag(self.model, model_id, Tag, tag_id)

    async def delete_mailout_phone_code(self, model_id: int, phone_code_id: int) -> Optional[MailoutRead]:
        return await super().delete_model_phone_code(self.model, model_id, PhoneCode, phone_code_id)
