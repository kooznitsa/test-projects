from datetime import datetime, time

from sqlmodel import Session
from sqlalchemy import select

from db.sessions import engine
from schemas.phone_codes import PhoneCode, PhoneCodeCreate
from schemas.timezones import Timezone, TimezoneCreate
from schemas.tags import Tag, TagCreate
from schemas.messages import Message, MessageCreate
from schemas.customers import Customer, CustomerCreate
from schemas.mailouts import Mailout, MailoutCreate
from schemas.users import User


def add_to_db(session, item):
    session.add(item)
    session.commit()
    session.refresh(item)


def upsert_value(session, result, model_from_orm):
    if result is None:
        result = model_from_orm
    for k, v in model_from_orm.dict(exclude_unset=True).items():
        setattr(result, k, v)
    add_to_db(session, result)
    return result


def upsert_phone_code(session, value):
    statement = select(PhoneCode).where(PhoneCode.phone_code == value)
    result = session.exec(statement).first()

    return upsert_value(
        session,
        result,
        PhoneCode.from_orm(PhoneCodeCreate(phone_code=value))
    )


def upsert_timezone(session, value):
    statement = select(Timezone).where(Timezone.timezone == value)
    result = session.exec(statement).first()

    return upsert_value(
        session,
        result,
        Timezone.from_orm(TimezoneCreate(timezone=value))
    )


def upsert_tag(session, value):
    statement = select(Tag).where(Tag.tag == value)
    result = session.exec(statement).first()

    return upsert_value(
        session,
        result,
        Tag.from_orm(TagCreate(tag=value))
    )


def create_entries(session):
    phone_code1 = upsert_phone_code(session, 925)
    phone_code2 = upsert_phone_code(session, 980)
    phone_code3 = upsert_phone_code(session, 967)

    timezone1 = upsert_timezone(session, 'Europe/Moscow')
    timezone2 = upsert_timezone(session, 'Europe/Belgrade')

    tag1 = upsert_tag(session, 'Female')
    tag2 = upsert_tag(session, 'Unemployed')
    tag3 = upsert_tag(session, 'Male')
    tag4 = upsert_tag(session, 'Student')

    customer1 = Customer.from_orm(
        CustomerCreate(
            country_code=7,
            phone=1234567,
        ),
        update={
            'phone_code_id': phone_code1.id,
            'timezone_id': timezone1.id,
        }
    )
    customer1.tags.extend([tag1, tag2])
    add_to_db(session, customer1)

    customer2 = Customer.from_orm(
        CustomerCreate(
            country_code=7,
            phone=4444444,
        ),
        update={
            'phone_code_id': phone_code2.id,
            'timezone_id': timezone2.id,
        }
    )
    customer2.tags.extend([tag3, tag4])
    add_to_db(session, customer2)

    mailout = Mailout.from_orm(
        MailoutCreate(
            start_time=datetime(2023, 6, 30, 10, 0, 0),
            finish_time=datetime(2023, 6, 30, 11, 0, 0),
            available_start=time(10, 0, 0),
            available_finish=time(19, 0, 0),
        )
    )
    mailout.tags.extend([tag1, tag2, tag3, tag4])
    mailout.phone_codes.extend([phone_code1, phone_code2, phone_code3])
    add_to_db(session, mailout)

    message = Message.from_orm(
        MessageCreate(
            text_message='Hello world',
            mailout_id=1,
            customer_id=1,
        )
    )
    add_to_db(session, message)

    user = User(username='shark')
    user.set_password('qwerty')
    add_to_db(session, user)


def add_sample_data():
    with Session(engine) as session:
        create_entries(session)
