from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status

from db.errors import EntityDoesNotExist
from db.sessions import async_engine, get_async_session, get_repository
from repositories.customers import CustomerRepository
from schemas.customers import Customer, CustomerCreate, CustomerRead

router = APIRouter(prefix='/customers')


@router.post(
    '/',
    response_model=CustomerRead,
    status_code=status.HTTP_201_CREATED,
    name='create_customer',
)
async def create_customer(
    customer_create: CustomerCreate = Body(...),
    repository: CustomerRepository = Depends(get_repository(CustomerRepository)),
) -> CustomerRead:
    """http://localhost:8000/api/customers"""
    try:
        return await repository.create(customer_create=customer_create)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Phone code or timezone not found'
        )


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
        result = await repository.get(customer_id=customer_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Customer with ID={customer_id} not found'
        )
    return result


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
