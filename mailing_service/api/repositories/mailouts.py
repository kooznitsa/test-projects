from typing import Optional

from sqlalchemy.orm import selectinload
from sqlmodel import select

from db.errors import EntityDoesNotExist
from repositories.base import BaseRepository
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
        offset: int = 0,
    ) -> list[MailoutRead]:
        query = select(self.model).order_by(self.model.id)
        if tag:
            query = query.where(self.model.tags.any(Tag.tag == tag))
        query = query.offset(offset).limit(limit)

        results = await self.session.exec(
            query.options(selectinload(self.model.tags))
        )
        return results.all()

    async def get(self, model_id: int) -> Optional[MailoutRead]:
        if mailout := await self._get_instance(self.model, model_id):
            return await self._get_instance_with_related(self.model, mailout)
        else:
            raise EntityDoesNotExist

    async def update(self, model_id: int, model_update: MailoutUpdate) -> Optional[MailoutRead]:
        item = await super().update(self.model, model_id, model_update, self.model_read)
        return await self._get_instance_with_related(self.model, item)
