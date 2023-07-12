import random

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from db.errors import EntityDoesNotExist
from repositories.messages import MessageRepository
from schemas.base import StatusEnum
from schemas.messages import Message, MessageCreate, MessageUpdate
from tests.test_repositories.test_customers import create_customer
from tests.test_repositories.test_mailouts import create_mailout


async def create_message(db_session: AsyncSession):
    _, _, db_mailout = await create_mailout(db_session)
    _, _, db_customer = await create_customer(db_session)

    repository = MessageRepository(db_session)

    message = MessageCreate(
        text_message='Hello world',
        mailout_id=db_mailout.id,
        customer_id=db_customer.id
    )

    db_message = await repository.create(message)

    return repository, message, db_message


@pytest.mark.asyncio
async def test_create_message(db_session: AsyncSession):
    _, message, db_message = await create_message(db_session)

    assert db_message.text_message == message.text_message
    assert db_message.created_at is not None
    assert db_message.status == StatusEnum.created
    assert db_message.mailout_id == message.mailout_id
    assert db_message.customer_id == message.customer_id


@pytest.mark.asyncio
async def test_get_messages(db_session: AsyncSession):
    repository, message, db_message = await create_message(db_session)

    db_messages = await repository.list()

    assert db_messages[0].text_message == message.text_message
    assert db_messages[0].created_at is not None
    assert db_messages[0].status == StatusEnum.created
    assert db_messages[0].mailout_id == message.mailout_id
    assert db_messages[0].customer_id == message.customer_id


@pytest.mark.asyncio
async def test_get_message_by_id(db_session: AsyncSession):
    repository, _, db_message = await create_message(db_session)

    found_message = await repository.get(model_id=db_message.id)

    assert db_message == found_message


@pytest.mark.asyncio
async def test_get_message_by_id_not_found(db_session: AsyncSession):
    repository = MessageRepository(db_session)

    with pytest.raises(expected_exception=EntityDoesNotExist):
        await repository.get(model_id=random.randint(2, 9))


@pytest.mark.asyncio
async def test_update_message(db_session: AsyncSession):
    new_text_message = 'Test message'
    new_mailout_id = 1
    new_customer_id = 1

    repository, _, db_message = await create_message(db_session)

    update_message = await repository.update(
        model_id=db_message.id,
        model_update=MessageUpdate(
            text_message=new_text_message,
            mailout_id=new_mailout_id,
            customer_id=new_customer_id
        ),
    )

    assert update_message.id == db_message.id
    assert update_message.text_message == new_text_message
    assert update_message.mailout_id == new_mailout_id
    assert update_message.customer_id == new_customer_id


@pytest.mark.asyncio
async def test_delete_message(db_session: AsyncSession):
    repository, _, db_message = await create_message(db_session)

    delete_message = await repository.delete(model_id=db_message.id)

    assert delete_message.status == StatusEnum.deleted
