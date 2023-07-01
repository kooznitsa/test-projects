from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status

from db.errors import EntityDoesNotExist
from db.sessions import async_engine, get_async_session, get_repository
from repositories.customers import CustomerRepository
from repositories.tags import TagRepository
from schemas.customers import Customer, CustomerCreate, CustomerRead, CustomerUpdate
from schemas.tags import Tag, TagCreate, TagRead, TagUpdate

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
    try:
        return await repository.create(model_create=customer_create)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Phone code or timezone not found'
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
    limit: int = Query(default=50, lte=100),
    offset: int = Query(default=0),
    repository: CustomerRepository = Depends(get_repository(CustomerRepository))
) -> list[Optional[CustomerRead]]:
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
    try:
        result = await repository.get(model_id=customer_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Customer with ID={customer_id} not found'
        )
    return result


@router.put(
    '/{customer_id}',
    response_model=CustomerRead,
    status_code=status.HTTP_200_OK,
    name='update_customer',
)
async def update_customer(
    customer_id: int,
    customer_update: CustomerUpdate = Body(...),
    repository: CustomerRepository = Depends(get_repository(CustomerRepository)),
) -> CustomerRead:
    try:
        await repository.get(model_id=customer_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Customer with ID={customer_id} not found'
        )
    return await repository.update(model_id=customer_id, model_update=customer_update)


@router.delete(
    '/{customer_id}',
    status_code=status.HTTP_200_OK,
    name='delete_customer',
)
async def delete_customer(
    customer_id: int,
    repository: CustomerRepository = Depends(get_repository(CustomerRepository)),
) -> None:
    try:
        await repository.get(model_id=customer_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Customer with ID={customer_id} not found'
        )
    return await repository.delete(model=Customer, model_id=customer_id)


@router.post(
    '/{customer_id}/tags',
    response_model=TagRead,
    status_code=status.HTTP_201_CREATED,
    name='create_customer_tag',
)
async def create_customer_tag(
    customer_id: int,
    tag_create: TagCreate = Body(...),
    repository: TagRepository = Depends(get_repository(TagRepository)),
) -> TagRead:
    try:
        return await repository.create(
            model_id=customer_id, tag_create=tag_create, parent_model=Customer
        )
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Customer with ID={customer_id} not found'
        )


@router.post(
    '/{customer_id}/tags/{tag_id}',
    response_model=CustomerRead,
    status_code=status.HTTP_201_CREATED,
    name='delete_customer_tag',
)
async def delete_customer_tag(
    customer_id: int,
    tag_id: int,
    repository: CustomerRepository = Depends(get_repository(CustomerRepository)),
) -> CustomerRead:
    try:
        return await repository.delete_customer_tag(
            tag_id=tag_id, model_id=customer_id
        )
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Customer or tag not found'
        )
