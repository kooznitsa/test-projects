from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status

from db.errors import EntityDoesNotExist
from db.sessions import async_engine, get_async_session, get_repository
from repositories.timezones import TimezoneRepository
from schemas.timezones import TimezoneCreate, TimezoneRead, TimezoneUpdate

router = APIRouter(prefix='/timezones')


@router.post(
    '/',
    response_model=TimezoneRead,
    status_code=status.HTTP_201_CREATED,
    name='create_timezone',
)
async def create_timezone(
    timezone_create: TimezoneCreate = Body(...),
    repository: TimezoneRepository = Depends(get_repository(TimezoneRepository)),
) -> TimezoneRead:
    """http://localhost:8000/api/timezones"""
    return await repository.create(timezone_create=timezone_create)


@router.get(
    '/',
    response_model=list[Optional[TimezoneRead]],
    status_code=status.HTTP_200_OK,
    name='get_timezones',
)
async def get_timezones(
    limit: int = Query(default=10, lte=100),
    offset: int = Query(default=0),
    repository: TimezoneRepository = Depends(get_repository(TimezoneRepository))
) -> list[Optional[TimezoneRead]]:
    """http://localhost:8000/api/timezones"""
    return await repository.list(
        limit=limit,
        offset=offset,
    )


@router.get(
    '/{timezone_id}',
    response_model=TimezoneRead,
    status_code=status.HTTP_200_OK,
    name='get_timezone',
)
async def get_timezone(
    timezone_id: int,
    repository: TimezoneRepository = Depends(get_repository(TimezoneRepository)),
) -> TimezoneRead:
    """http://localhost:8000/api/timezones/1"""
    try:
        result = await repository.get(timezone_id=timezone_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Timezone with ID={timezone_id} not found'
        )
    return result


@router.put(
    '/{timezone_id}',
    response_model=TimezoneRead,
    status_code=status.HTTP_200_OK,
    name='update_timezone',
)
async def update_timezone(
    timezone_id: int,
    timezone_update: TimezoneUpdate = Body(...),
    repository: TimezoneRepository = Depends(get_repository(TimezoneRepository)),
) -> TimezoneRead:
    """http://localhost:8000/api/timezones/1"""
    try:
        await repository.get(timezone_id=timezone_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Timezone with ID={timezone_id} not found'
        )
    return await repository.update(timezone_id=timezone_id, timezone_update=timezone_update)


@router.delete(
    '/{timezone_id}',
    status_code=status.HTTP_200_OK,
    name='delete_timezone',
)
async def delete_timezone(
    timezone_id: int,
    repository: TimezoneRepository = Depends(get_repository(TimezoneRepository)),
) -> None:
    """http://localhost:8000/api/timezones/1"""
    try:
        await repository.get(timezone_id=timezone_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Timezone with ID={timezone_id} not found'
        )
    return await repository.delete(timezone_id=timezone_id)
