from datetime import datetime, time
import random

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from db.errors import EntityDoesNotExist
from repositories.phone_codes import PhoneCodeRepository
from repositories.tags import TagRepository
from repositories.mailouts import MailoutRepository
from schemas.phone_codes import PhoneCodeCreate
from schemas.tags import TagCreate
from schemas.mailouts import Mailout, MailoutCreate, MailoutUpdate


async def create_mailout(db_session: AsyncSession):
    mailout_repo = MailoutRepository(db_session)
    tag_repo = TagRepository(db_session)
    phone_code_repo = PhoneCodeRepository(db_session)

    mailout = MailoutCreate(
        start_time=datetime(2023, 7, 12),
        finish_time=datetime(2023, 7, 13),
        available_start=time(9, 0, 0),
        available_finish=time(18, 0, 0)
    )

    db_mailout = await mailout_repo.create(mailout)

    db_tag = await tag_repo.create(
        model_id=db_mailout.id,
        tag_create=TagCreate(tag='Test'),
        parent_model=Mailout,
    )

    db_phone_code = await phone_code_repo.create(
        model_id=db_mailout.id,
        model_create=PhoneCodeCreate(phone_code=888),
        parent_model=Mailout,
    )

    return mailout_repo, mailout, db_mailout


@pytest.mark.asyncio
async def test_create_mailout(db_session: AsyncSession):
    _, mailout, db_mailout = await create_mailout(db_session)

    assert db_mailout.start_time == mailout.start_time
    assert db_mailout.finish_time == mailout.finish_time
    assert db_mailout.available_start == mailout.available_start
    assert db_mailout.available_finish == mailout.available_finish


@pytest.mark.asyncio
async def test_get_mailouts(db_session: AsyncSession):
    repository, mailout, db_mailout = await create_mailout(db_session)

    db_mailouts = await repository.list()

    assert db_mailouts[0].start_time == mailout.start_time
    assert db_mailouts[0].finish_time == mailout.finish_time
    assert db_mailouts[0].available_start == mailout.available_start
    assert db_mailouts[0].available_finish == mailout.available_finish


@pytest.mark.asyncio
async def test_get_mailout_by_id(db_session: AsyncSession):
    repository, _, db_mailout = await create_mailout(db_session)

    found_mailout = await repository.get(model_id=db_mailout.id)

    assert db_mailout == found_mailout


@pytest.mark.asyncio
async def test_get_mailout_by_id_not_found(db_session: AsyncSession):
    repository = MailoutRepository(db_session)

    with pytest.raises(expected_exception=EntityDoesNotExist):
        await repository.get(model_id=random.randint(2, 9))


@pytest.mark.asyncio
async def test_update_mailout(db_session: AsyncSession):
    new_start_time = datetime(2024, 7, 12)
    new_finish_time = datetime(2024, 7, 13)
    new_available_start = time(8, 0, 0)
    new_available_finish = time(19, 0, 0)

    repository, _, db_mailout = await create_mailout(db_session)

    update_mailout = await repository.update(
        model_id=db_mailout.id,
        model_update=MailoutUpdate(
            start_time=new_start_time,
            finish_time=new_finish_time,
            available_start=new_available_start,
            available_finish=new_available_finish,
        ),
    )

    assert update_mailout.id == db_mailout.id
    assert update_mailout.start_time == new_start_time
    assert update_mailout.finish_time == new_finish_time
    assert update_mailout.available_start == new_available_start
    assert update_mailout.available_finish == new_available_finish


@pytest.mark.asyncio
async def test_delete_mailout(db_session: AsyncSession):
    repository, _, db_mailout = await create_mailout(db_session)

    delete_mailout = await repository.delete(model_id=db_mailout.id, model=Mailout)

    assert delete_mailout is None
    with pytest.raises(expected_exception=EntityDoesNotExist):
        await repository.get(model_id=db_mailout.id)


@pytest.mark.asyncio
async def test_delete_mailout_tag(db_session: AsyncSession):
    repository, _, db_mailout = await create_mailout(db_session)

    repository.delete_mailout_tag(model_id=1, tag_id=1)

    assert len(db_mailout.tags) == 1


@pytest.mark.asyncio
async def test_delete_mailout_phone_code(db_session: AsyncSession):
    repository, _, db_mailout = await create_mailout(db_session)

    repository.delete_mailout_phone_code(model_id=1, phone_code_id=1)

    assert len(db_mailout.phone_codes) == 1
