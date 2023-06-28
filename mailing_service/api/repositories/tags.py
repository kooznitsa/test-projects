from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db.errors import EntityDoesNotExist
from repositories.base import BaseRepository
from schemas.tags import Tag, TagCreate, TagRead, TagUpdate


class TagRepository(BaseRepository):
    model = Tag
    model_read = TagRead

    async def create(self, model_id: int, tag_create: TagCreate, model) -> TagRead:
        model_query = await self.session.scalars(
            select(model)
            .where(model.id == model_id)
            .options(selectinload(model.tags))
        )

        if item := model_query.first():
            tag_query = select(Tag).where(Tag.tag == tag_create.tag)
            result = await self.session.exec(tag_query)
            new_tag = await self._upsert_value(result.scalars().first(), Tag, tag_create)
            self.session.add(new_tag)
            item.tags.append(new_tag)
            await self.session.commit()
            await self.session.refresh(new_tag)
            return new_tag
        else:
            raise EntityDoesNotExist

    async def get(self, model_id: int) -> Optional[TagRead]:
        return await super().get(self.model, model_id)

    async def update(self, model_id: int, model_update: TagUpdate) -> Optional[TagRead]:
        return await super().update(self.model, model_id, model_update, self.model_read)
