from datetime import datetime, time

import pytest
from fastapi import status


async def create_mailout(async_client_authenticated):
    mailout = {
        'start_time': datetime(2023, 7, 12).isoformat(),
        'finish_time': datetime(2023, 7, 13).isoformat(),
        'available_start': time(9, 0, 0).isoformat(),
        'available_finish': time(18, 0, 0).isoformat()
    }
    response = await async_client_authenticated.post(
        '/api/mailouts/',
        json=mailout,
    )

    return mailout, response


async def create_mailouts(async_client_authenticated, qty: int = 1):
    return [
        await create_mailout(async_client_authenticated)
        for _ in range(qty)
    ]


@pytest.mark.asyncio
async def test_get_mailouts(async_client):
    response = await async_client.get('/api/mailouts/')
    mailouts = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0
    assert all(['start_time' in m for m in mailouts])


@pytest.mark.asyncio
async def test_create_mailout(async_client_authenticated):
    mailout, response = await create_mailout(async_client_authenticated)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['start_time'] == mailout['start_time']
    assert response.json()['finish_time'] == mailout['finish_time']
    assert response.json()['available_start'] == mailout['available_start']
    assert response.json()['available_finish'] == mailout['available_finish']


@pytest.mark.asyncio
async def test_get_mailout(async_client_authenticated, async_client):
    mailout, response_create = await create_mailout(async_client_authenticated)

    response = await async_client.get(
        f"/api/mailouts/{response_create.json()['id']}"
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['start_time'] == mailout['start_time']
    assert response.json()['finish_time'] == mailout['finish_time']
    assert response.json()['available_start'] == mailout['available_start']
    assert response.json()['available_finish'] == mailout['available_finish']
    assert response.json()['id'] == response_create.json()['id']


@pytest.mark.asyncio
async def test_delete_mailout(async_client_authenticated):
    _, response_create = await create_mailout(async_client_authenticated)

    response = await async_client_authenticated.delete(
        f"/api/mailouts/{response_create.json()['id']}"
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_update_mailout(async_client_authenticated):
    mailout, response_create = await create_mailout(async_client_authenticated)

    new_start_time = datetime(2024, 7, 12).isoformat()
    new_finish_time = datetime(2024, 7, 13).isoformat()
    new_available_start = time(8, 0, 0).isoformat()
    new_available_finish = time(19, 0, 0).isoformat()

    response = await async_client_authenticated.put(
        f"/api/mailouts/{response_create.json()['id']}",
        json={
            'start_time': new_start_time,
            'finish_time': new_finish_time,
            'available_start': new_available_start,
            'available_finish': new_available_finish
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['start_time'] == new_start_time
    assert response.json()['finish_time'] == new_finish_time
    assert response.json()['available_start'] == new_available_start
    assert response.json()['available_finish'] == new_available_finish
    assert response.json()['id'] == response_create.json()['id']


@pytest.mark.asyncio
async def test_get_mailout_paginated(async_client, async_client_authenticated):
    await create_mailouts(async_client_authenticated, qty=4)

    response_page_1 = await async_client.get('/api/mailouts/?limit=2')
    assert len(response_page_1.json()) == 2

    response_page_2 = await async_client.get(
        '/api/mailouts/?limit=2&offset=2'
    )
    assert len(response_page_2.json()) == 2

    response = await async_client.get('/api/mailouts/')
    assert len(response.json()) == 4


@pytest.mark.asyncio
async def test_create_mailout_tag(async_client_authenticated):
    mailout, response_create = await create_mailout(async_client_authenticated)

    response = await async_client_authenticated.post(
        f'/api/mailouts/{response_create.json()["id"]}/tags',
        json={'tag': 'Test'}
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_delete_mailout_tag(async_client_authenticated):
    mailout, response_create = await create_mailout(async_client_authenticated)

    tag_created = await async_client_authenticated.post(
        f'/api/mailouts/{response_create.json()["id"]}/tags',
        json={'tag': 'Test'}
    )

    response = await async_client_authenticated.post(
        f'/api/mailouts/{response_create.json()["id"]}/tags/{tag_created.json()["id"]}'
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_create_mailout_phone_code(async_client_authenticated):
    mailout, response_create = await create_mailout(async_client_authenticated)

    response = await async_client_authenticated.post(
        f'/api/mailouts/{response_create.json()["id"]}/phone_codes',
        json={'phone_code': 888}
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_delete_mailout_phone_code(async_client_authenticated):
    mailout, response_create = await create_mailout(async_client_authenticated)

    phone_code_created = await async_client_authenticated.post(
        f'/api/mailouts/{response_create.json()["id"]}/phone_codes',
        json={'phone_code': 888}
    )

    response = await async_client_authenticated.post(
        f'/api/mailouts/{response_create.json()["id"]}/phone_codes/{phone_code_created.json()["id"]}'
    )

    assert response.status_code == status.HTTP_200_OK
