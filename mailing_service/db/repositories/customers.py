from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from api.schemas.customers import Customer, CustomerOutput


class CustomerRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(
        self,
        tag: str | None = None,
        phone_code: int | None = None,
        limit: int = 10,
        offset: int = 0
    ) -> list[CustomerOutput]:
        query = select(Customer)
        if tag:
            query = query.where(any(i.tag == tag for i in Customer.tags))
        if phone_code:
            query = query.where(Customer.phone_code == phone_code)
        results = await self.session.exec(query.offset(offset).limit(limit))
        return [CustomerOutput(**customer.dict()) for customer in results]
