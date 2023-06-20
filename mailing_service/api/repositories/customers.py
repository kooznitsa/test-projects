from typing import Optional

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import Session, col

from db.errors import EntityDoesNotExist
from schemas.customers import Customer, CustomerRead


class CustomerRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_instance(self, customer_id: int):
        query = (
            select(Customer)
            .where(Customer.id == customer_id)
        )
        results = await self.session.exec(query)
        return results.first()

    async def list(
        self,
        tag: Optional[str] = None,
        phone_code: int | None = None,
        limit: int = 10,
        offset: int = 0
    ) -> list[CustomerRead]:
        query = select(Customer)
        if tag:
            # raise NotImplementedError(str(op))
            # 2023-06-20 16:57:57 fastapi_service  | NotImplementedError: <built-in function getitem>
            query = query.where(any(i.tag == tag for i in Customer.tags))
        if phone_code:
            query = query.where(Customer.phone_code == phone_code)
        results = await self.session.exec(query.offset(offset).limit(limit))
        return [CustomerRead(**customer.dict()) for customer in results]

    async def get(self, customer_id: int) -> Optional[CustomerRead]:
        db_customer = await self._get_instance(customer_id)

        if db_customer is None:
            raise EntityDoesNotExist

        return CustomerRead(**db_customer.dict())
