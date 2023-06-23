from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status

from db.errors import EntityDoesNotExist
from db.sessions import async_engine, get_async_session, get_repository
from repositories.phone_codes import PhoneCodeRepository
from schemas.phone_codes import PhoneCodeCreate, PhoneCodeRead

router = APIRouter(prefix='/phone_codes')


@router.post(
    '/',
    response_model=PhoneCodeRead,
    status_code=status.HTTP_201_CREATED,
    name='create_phone_code',
)
async def create_phone_code(
    phone_code_create: PhoneCodeCreate = Body(...),
    repository: PhoneCodeRepository = Depends(get_repository(PhoneCodeRepository)),
) -> PhoneCodeRead:
    """http://localhost:8000/api/phone_codes"""
    return await repository.create(phone_code_create=phone_code_create)


@router.get(
    '/',
    response_model=list[Optional[PhoneCodeRead]],
    status_code=status.HTTP_200_OK,
    name='get_phone_codes',
)
async def get_phone_codes(
    limit: int = Query(default=10, lte=100),
    offset: int = Query(default=0),
    repository: PhoneCodeRepository = Depends(get_repository(PhoneCodeRepository))
) -> list[Optional[PhoneCodeRead]]:
    """http://localhost:8000/api/phone_codes"""
    return await repository.list(
        limit=limit,
        offset=offset,
    )


@router.get(
    '/{phone_code_id}',
    response_model=PhoneCodeRead,
    status_code=status.HTTP_200_OK,
    name='get_phone_code',
)
async def get_phone_code(
    phone_code_id: int,
    repository: PhoneCodeRepository = Depends(get_repository(PhoneCodeRepository)),
) -> PhoneCodeRead:
    """http://localhost:8000/api/phone_codes/1"""
    try:
        result = await repository.get(phone_code_id=phone_code_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Phone code with ID={phone_code_id} not found'
        )
    return result
