from datetime import datetime
from typing import Optional

from sqlmodel import select

from db.errors import EntityDoesNotExist
from repositories.base import BaseRepository
from schemas.base import StatusEnum
from schemas.customers import Customer
from schemas.mailouts import Mailout
from schemas.messages import Message, MessageCreate, MessageRead, MessageUpdate


class MessageRepository(BaseRepository):
    model = Message

    async def create(self, model_create: MessageCreate) -> MessageRead:
        customer_query = await self.session.exec(
            select(Customer)
            .where(Customer.id == model_create.customer_id)
        )
        customer = customer_query.first()
        mailout_query = await self.session.exec(
            select(Mailout)
            .where(Mailout.id == model_create.mailout_id)
        )
        mailout = mailout_query.first()

        if not customer or not mailout:
            raise EntityDoesNotExist
        else:
            return await self._create_not_unique(self.model, model_create)

    async def list(self, limit: int = 50, offset: int = 0) -> list[MessageRead]:
        return await super().list(self.model, limit, offset)

    async def get(self, model_id: int) -> Optional[MessageRead]:
        return await super().get(self.model, model_id)

    async def update(self, model_id: int, model_update: MessageUpdate) -> Optional[MessageRead]:
        if item := await self._get_instance(self.model, model_id):
            item_dict = model_update.dict(
                exclude_unset=True,
                exclude={'id', 'status', 'created_at'},
            )
            for key, value in item_dict.items():
                setattr(item, key, value)

            setattr(item, 'status', StatusEnum.updated)
            setattr(item, 'created_at', datetime.now())

            await self._add_to_db(item)
            return await self._get_instance(self.model, model_id)
        else:
            raise EntityDoesNotExist

    async def delete(self, model_id: int) -> None:
        if item := await self._get_instance(self.model, model_id):
            setattr(item, 'status', StatusEnum.deleted)
            await self._add_to_db(item)
            return await self._get_instance(self.model, model_id)
        else:
            raise EntityDoesNotExist
