from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession

from db.errors import EntityDoesNotExist


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_instance(self, model, model_id: int):
        query = select(model).where(model.id == model_id)
        results = await self.session.exec(query)
        return results.scalars().first()

    async def _get_instance_with_related(self, model, item):
        try:
            options = selectinload(model.tags).selectinload(model.phone_codes)
        except AttributeError:
            options = selectinload(model.tags)

        result = await self.session.scalars(
            select(model)
            .where(model.id == item.id)
            .options(options)
        )
        return result.first()

    async def _add_to_db(self, new_item):
        self.session.add(new_item)
        await self.session.commit()
        await self.session.refresh(new_item)

    async def _upsert(self, query, model, model_create):
        result = await self.session.exec(query)
        result = result.scalars().first()
        model_from_orm = model.from_orm(model_create)

        if result is None:
            result = model_from_orm

        for k, v in model_from_orm.dict(exclude_unset=True).items():
            setattr(result, k, v)
        return result

    async def _create_not_unique(self, model, model_create):
        new_item = model.from_orm(model_create)
        await self._add_to_db(new_item)
        return await self._get_instance_with_related(model, new_item)

    async def list(self, model, limit: int, offset: int = 0):
        query = select(model).order_by(model.id).offset(offset).limit(limit)
        results = await self.session.exec(query)
        return results.scalars().all()

    async def get(self, model, model_id: int):
        if item := await self._get_instance(model, model_id):
            return item
        else:
            raise EntityDoesNotExist

    async def update(self, model, model_id: int, model_update, model_read_instance):
        if item := await self._get_instance(model, model_id):
            item_dict = model_update.dict(
                exclude_unset=True,
                exclude={'id'},
            )
            for key, value in item_dict.items():
                setattr(item, key, value)
            await self._add_to_db(item)
            return model_read_instance(**item.dict())
        else:
            raise EntityDoesNotExist

    async def delete(self, model, model_id: int) -> None:
        if item := await self._get_instance(model, model_id):
            await self.session.delete(item)
            await self.session.commit()
        else:
            raise EntityDoesNotExist
