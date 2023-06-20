from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel.ext.asyncio.session import AsyncSession

from db.errors import EntityDoesNotExist
from db.sessions import async_engine, get_async_session, get_repository
from repositories.customers import CustomerRepository
from schemas.tags import Tag, TagCreate
from schemas.customers import Customer, CustomerCreate, CustomerRead

router = APIRouter(prefix='/customers')


# @router.get('/')
# async def get_customers(
#     tag: str | None = None,
#     phone_code: int | None = None,
#     session: AsyncSession = Depends(get_async_session)
# ) -> list:
#     """http://127.0.0.1:8000/api/customers?tag=Student&phone_code=936"""
#     query = select(Customer)
#     if tag:
#         query = query.where(any(i.tag == tag for i in Customer.tags))
#     if phone_code:
#         query = query.where(Customer.phone_code == phone_code)
#     # return session.exec(query).all() # if synchronous
#     results = await session.execute(query)
#     return results.scalars().all()

@router.get(
    '/',
    response_model=list[Optional[CustomerRead]],
    status_code=status.HTTP_200_OK,
    name='get_customers',
)
async def get_customers(
    tag: str | None = Query(default=None),
    phone_code: int | None = Query(default=None),
    limit: int = Query(default=10, lte=100),
    offset: int = Query(default=0),
    repository: CustomerRepository = Depends(get_repository(CustomerRepository))
) -> list[Optional[CustomerRead]]:
    """http://localhost:8000/api/customers/?tag=Woman&phone_code=925&limit=10&offset=0"""
    return await repository.list(
        tag=tag,
        phone_code=phone_code,
        limit=limit,
        offset=offset,
    )


@router.get(
    '/{customer_id}',
    response_model=CustomerRead,
    status_code=status.HTTP_200_OK,
    name='get_customer',
)
async def get_customer(
    customer_id: int,
    repository: CustomerRepository = Depends(get_repository(CustomerRepository)),
) -> CustomerRead:
    """http://localhost:8000/api/customers/1"""
    try:
        await repository.get(customer_id=customer_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Customer not found'
        )
    return await repository.get(customer_id=customer_id)


# @router.post('/', response_model=Customer)
# async def add_customer(customer_input: CustomerInput) -> Customer:
#     with AsyncSession(async_engine) as session:
#         new_customer = await Customer.from_orm(customer_input)
#         await session.add(new_customer)
#         await session.commit()
#         await session.refresh(new_customer)
#         return new_customer
#
#
# @router.delete('/{id}', status_code=204)
# async def remove_customer(
#     id: int,
#     session: AsyncSession = Depends(get_async_session)
# ) -> None:
#     if customer := await session.get(Customer, id):
#         await session.delete(customer)
#         await session.commit()
#     else:
#         raise HTTPException(
#             status_code=404,
#             detail=f'No customer with ID {id} is found.'
#         )
#
#
# @router.put('/{id}', response_model=Customer)
# async def change_customer(
#     id: int,
#     new_data: CustomerInput,
#     session: AsyncSession = Depends(get_async_session)
# ) -> Customer:
#     if customer := await session.get(Customer, id):
#         customer.phone = new_data.phone
#         customer.phone_code = new_data.phone_code
#         customer.timezone = new_data.timezone
#         await session.commit()
#         return customer
#     else:
#         raise HTTPException(
#             status_code=404,
#             detail=f'No customer with ID {id} is found.'
#         )
#
#
# @router.post('/{customer_id}/tags', response_model=Tag)
# async def add_customer_tag(
#     customer_id: int,
#     tag_input: TagInput,
#     session: AsyncSession = Depends(get_async_session)
# ) -> Tag:
#     if customer := await session.get(Customer, customer_id):
#         new_tag = Tag.from_orm(tag_input, update={'customer_id': customer_id})
#         customer.tags.append(new_tag)
#         await session.commit()
#         await session.refresh(new_tag)
#         return new_tag
#     else:
#         raise HTTPException(
#             status_code=404,
#             detail=f'No customer with ID {customer_id} is found.'
#         )
