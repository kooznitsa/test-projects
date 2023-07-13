import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_login_user(create_user, async_client):
    await create_user()

    response = await async_client.post(
        '/auth/token',
        data={'username': 'shark', 'password': 'qwerty'},
    )

    assert response.status_code == status.HTTP_200_OK
