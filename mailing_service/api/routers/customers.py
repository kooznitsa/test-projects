from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status

from db.errors import EntityDoesNotExist
from db.sessions import async_engine, get_async_session, get_repository
from repositories.customers import CustomerRepository
from repositories.tags import TagRepository
from schemas.customers import Customer, CustomerCreate, CustomerRead, CustomerUpdate
from schemas.tags import TagCreate, TagRead, TagUpdate

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
    limit: int = Query(default=50, lte=100),
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
    """http://localhost:8000/api/customers/1"""
    try:
        await repository.get(customer_id=customer_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Customer with ID={customer_id} not found'
        )
    return await repository.update(customer_id=customer_id, customer_update=customer_update)


@router.delete(
    '/{customer_id}',
    status_code=status.HTTP_200_OK,
    name='delete_customer',
)
async def delete_customer(
    customer_id: int,
    repository: CustomerRepository = Depends(get_repository(CustomerRepository)),
) -> None:
    """http://localhost:8000/api/customers/1"""
    try:
        await repository.get(customer_id=customer_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Customer with ID={customer_id} not found'
        )
    return await repository.delete(customer_id=customer_id)


@router.post(
    '/{customer_id}/tags',
    response_model=TagRead,
    status_code=status.HTTP_201_CREATED,
    name='create_tag',
)
async def create_tag(
    customer_id: int,
    tag_create: TagCreate = Body(...),
    repository: TagRepository = Depends(get_repository(TagRepository)),
) -> TagRead:
    """http://localhost:8000/api/customers/1/tags"""
    try:
        return await repository.create(model_id=customer_id, tag_create=tag_create, model=Customer)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Customer with ID={customer_id} not found'
        )


@router.put(
    '/{customer_id}/tags/{tag_id}',
    response_model=TagRead,
    status_code=status.HTTP_200_OK,
    name='update_tag',
)
async def update_tag(
    tag_id: int,
    tag_update: TagUpdate = Body(...),
    repository: TagRepository = Depends(get_repository(TagRepository)),
) -> TagRead:
    """http://localhost:8000/api/customers/1/tags/1"""
    try:
        await repository.get(tag_id=tag_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Tag with ID={tag_id} not found'
        )
    return await repository.update(tag_id=tag_id, tag_update=tag_update)


@router.delete(
    '/{customer_id}/tags/{tag_id}',
    status_code=status.HTTP_200_OK,
    name='delete_tag',
)
async def delete_tag(
    tag_id: int,
    repository: TagRepository = Depends(get_repository(TagRepository)),
) -> None:
    """http://localhost:8000/api/customers/1/tags/1"""
    try:
        await repository.get(tag_id=tag_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Tag with ID={tag_id} not found'
        )
    return await repository.delete(tag_id=tag_id)
