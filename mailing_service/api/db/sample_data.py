from datetime import datetime, time

from sqlmodel import Session
from sqlalchemy import inspect, select, text

from db.sessions import engine
from schemas.phone_codes import PhoneCode, PhoneCodeCreate
from schemas.timezones import Timezone, TimezoneCreate
from schemas.tags import Tag, TagCreate, TagRead
from schemas.messages import Message, MessageCreate
from schemas.customers import Customer, CustomerCreate, CustomerRead
from schemas.mailouts import Mailout, MailoutCreate


def upsert_value(session, result, model_from_orm):
    """Upsert a value.

    It is used to create a value in the database if it does not already exist,
    else it is used to update the existing one.

    Args:
      session:
        with Session(engine) as session: ...
      result:
        The model data.
      model_from_orm:
        The model from_orm(model_create) data.

    Returns:
      The upserted model.
    """

    # if the entity does not exist, create it
    if result is None:
        result = model_from_orm

    # sync the data
    for k, v in model_from_orm.dict(exclude_unset=True).items():
        setattr(result, k, v)

    # persist the data to the database
    session.add(result)
    session.commit()
    session.refresh(result)

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


def add_sample_data():
    with Session(engine) as session:
        phone_code1 = upsert_phone_code(session, 925)
        print(phone_code1)

        timezone = upsert_timezone(session, 'Europe/Moscow')
        print(timezone)

        tag1 = upsert_tag(session, 'Woman')
        tag2 = upsert_tag(session, 'Unemployed')
        print(tag1)

        customer1 = Customer.from_orm(
            CustomerCreate(
                country_code=7,
                phone=1234567,
            ),
            update={
                'phone_code_id': phone_code1.id,
                'timezone_id': timezone.id,
            }
        )

        print(customer1.tags)

        customer1.tags.extend([tag1, tag2])

        session.add(customer1)
        session.commit()
        session.refresh(customer1)

        mailout = Mailout.from_orm(
            MailoutCreate(
                start_time=datetime(2023, 6, 30, 10, 0, 0),
                finish_time=datetime(2023, 6, 30, 11, 0, 0),
                available_start=time(10, 0, 0),
                available_finish=time(19, 0, 0),
            )
        )
        mailout.tags.extend([tag1, tag2])
        mailout.phone_codes.extend([phone_code1])

        session.add(mailout)
        session.commit()
        session.refresh(mailout)
