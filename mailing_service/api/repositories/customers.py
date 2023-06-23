from typing import Optional

from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.errors import EntityDoesNotExist
from schemas.phone_codes import PhoneCode, PhoneCodeCreate, PhoneCodeRead
from schemas.timezones import Timezone, TimezoneCreate, TimezoneRead
from schemas.tags import Tag, TagCreate, TagRead
from schemas.customers import Customer, CustomerCreate, CustomerRead


class CustomerRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_instance(self, customer_id: int):
        query = (
            select(Customer)
            .where(Customer.id == customer_id)
        )
        result = await self.session.exec(
            query.options(selectinload(Customer.tags))
        )

        return result.first()

    async def create(self, customer_create: CustomerCreate) -> CustomerRead:
        phone_code_query = await self.session.exec(
            select(PhoneCode)
            .where(PhoneCode.id == customer_create.phone_code_id)
        )
        phone_code = phone_code_query.first()
        timezone_query = await self.session.execute(
            select(Timezone)
            .where(Timezone.id == customer_create.timezone_id)
        )
        timezone = timezone_query.first()

        if not phone_code or not timezone:
            raise EntityDoesNotExist
        else:
            customer = Customer.from_orm(customer_create)
            self.session.add(customer)
            await self.session.commit()
            await self.session.refresh(customer)

            # return customer

            result = await self.session.scalars(
                select(Customer)
                .where(Customer.id == customer.id)
                .options(selectinload(Customer.tags))
            )
            return result.first()

    async def list(
        self,
        tag: Optional[str] = None,
        phone_code: int | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> list[CustomerRead]:
        query = select(Customer).order_by(Customer.id)
        if tag:
            query = query.where(Customer.tags.any(Tag.tag == tag))
        if phone_code:
            query = (
                query.join(PhoneCode)
                .where(PhoneCode.id == Customer.phone_code_id)
                .where(PhoneCode.phone_code == phone_code)
            )
        query = query.offset(offset).limit(limit)

        results = await self.session.exec(
            query.options(selectinload(Customer.tags))
        )
        return results.all()

    async def get(self, customer_id: int) -> Optional[CustomerRead]:
        if customer := await self._get_instance(customer_id):
            return customer
        else:
            raise EntityDoesNotExist
