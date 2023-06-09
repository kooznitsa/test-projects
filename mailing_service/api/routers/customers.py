from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.sessions import async_engine, get_async_session
from api.schemas.customers import Customer, CustomerInput, CustomerOutput
from api.schemas.tags import Tag, TagInput

router = APIRouter(prefix='/api/customers')


@router.get('/')
async def get_customers(
    tag: str | None = None, 
    phone_code: int | None = None,
    session: AsyncSession = Depends(get_async_session)
) -> list:
    """http://127.0.0.1:8000/api/customers?tag=Student&phone_code=936"""
    query = select(Customer)
    if tag:
        query = query.where(any(i.tag == tag for i in Customer.tags))
    if phone_code:
        query = query.where(Customer.phone_code == phone_code)
    return await session.exec(query).all()


@router.get('/{id}', response_model=CustomerOutput)
async def get_customer_by_id(
    id: int, 
    session: AsyncSession = Depends(get_async_session)
) -> Customer:
    """http://127.0.0.1:8000/api/customers/2
    Path parameters cannot be optional arguments.
    You need to handle absent values in code.
    """
    if customer := await session.get(Customer, id):
        return customer
    else:
        raise HTTPException(
            status_code=404, 
            detail=f'No customer with ID {id} is found.'
        )
    

@router.post('/', response_model=Customer)
async def add_customer(customer_input: CustomerInput) -> Customer:
    with AsyncSession(async_engine) as session:
        new_customer = await Customer.from_orm(customer_input)
        await session.add(new_customer)
        await session.commit()
        await session.refresh(new_customer)
        return new_customer
    

@router.delete('/{id}', status_code=204)
async def remove_customer(
    id: int, 
    session: AsyncSession = Depends(get_async_session)
) -> None:
    if customer := await session.get(Customer, id):
        await session.delete(customer)
        await session.commit()
    else:
        raise HTTPException(
            status_code=404, 
            detail=f'No customer with ID {id} is found.'
        )
    

@router.put('/{id}', response_model=Customer)
async def change_customer(
    id: int, 
    new_data: CustomerInput,
    session: AsyncSession = Depends(get_async_session)
) -> Customer:
    if customer := await session.get(Customer, id):
        customer.phone = new_data.phone
        customer.phone_code = new_data.phone_code
        customer.timezone = new_data.timezone
        await session.commit()
        return customer
    else:
        raise HTTPException(
            status_code=404, 
            detail=f'No customer with ID {id} is found.'
        )
    

# @router.get('/tags/{tag}')
# async def get_customers_by_tag(tag: str):
#     """http://127.0.0.1:8000/api/customers/tags/Female"""
#     if result := [
#         customer for customer in customers_db 
#         if any(i.tag == tag for i in customer.tags)
#     ]:
#         return result
#     else:
#         raise HTTPException(
#             status_code=404, 
#             detail=f'No customers with tag {tag} are found.'
#         )


@router.post('/{customer_id}/tags', response_model=Tag)
async def add_tag(
    customer_id: int, 
    tag_input: TagInput,
    session: AsyncSession = Depends(get_async_session)
) -> Tag:
    if customer := await session.get(Customer, customer_id):
        new_tag = Tag.from_orm(tag_input, update={'customer_id': customer_id})
        customer.tags.append(new_tag)
        await session.commit()
        await session.refresh(new_tag)
        return new_tag
    else:
        raise HTTPException(
            status_code=404, 
            detail=f'No customer with ID {customer_id} is found.'
        )