from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db.errors import EntityDoesNotExist
from repositories.base_repository import BaseRepository
from schemas.tags import Tag, TagCreate, TagRead, TagUpdate
from schemas.customers import Customer


class TagRepository(BaseRepository):
    async def _get_instance(self, tag_id: int):
        query = select(Tag).where(Tag.id == tag_id)
        results = await self.session.exec(query)
        return results.scalars().first()

    async def create(self, model_id: int, tag_create: TagCreate, model) -> TagRead:
        model_query = await self.session.scalars(
            select(model)
            .where(model.id == model_id)
            .options(selectinload(model.tags))
        )
        entity = model_query.first()

        if entity:
            tag_query = select(Tag).where(Tag.tag == tag_create.tag)
            result = await self.session.exec(tag_query)
            new_tag = await self._upsert_value(result.scalars().first(), Tag, tag_create)
            self.session.add(new_tag)
            entity.tags.append(new_tag)
            await self.session.commit()
            await self.session.refresh(new_tag)
            return new_tag
        else:
            raise EntityDoesNotExist

    async def get(self, tag_id: int) -> Optional[TagRead]:
        if tag := await self._get_instance(tag_id):
            return tag
        else:
            raise EntityDoesNotExist

    async def update(
        self,
        tag_id: int,
        tag_update: TagUpdate,
    ) -> Optional[TagRead]:
        if tag := await self._get_instance(tag_id):
            tag_dict = tag_update.dict(
                exclude_unset=True,
                exclude={'id'},
            )
            for key, value in tag_dict.items():
                setattr(tag, key, value)
            self.session.add(tag)
            await self.session.commit()
            await self.session.refresh(tag)
            return TagRead(**tag.dict())
        else:
            raise EntityDoesNotExist

    async def delete(self, tag_id: int) -> None:
        if tag := await self._get_instance(tag_id):
            await self.session.delete(tag)
            await self.session.commit()
        else:
            raise EntityDoesNotExist
