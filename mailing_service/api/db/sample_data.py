from datetime import datetime, time
import inspect as inspect_func

from sqlmodel import Session
from sqlalchemy import inspect, select, text
from sqlalchemy.dialects.postgresql import insert

from db.sessions import engine
from schemas.phone_codes import PhoneCode, PhoneCodeCreate
from schemas.timezones import Timezone, TimezoneCreate
from schemas.tags import Tag, TagCreate
from schemas.messages import Message, MessageCreate
from schemas.customers import Customer, CustomerCreate
from schemas.mailouts import Mailout, MailoutCreate


# def insert_or_update(model, entities: set):
#     table = model.__table__
#     primary_keys = [key.name for key in inspect(table).primary_key]
#     stmt = (
#         insert(table)
#         .returning(text(primary_keys[0]))
#         .values([e.__dict__ for e in entities])
#     )
#     update_dict = {c.name: c for c in stmt.excluded if not c.primary_key}
#
#     if not update_dict:
#         raise ValueError(f'{inspect_func.stack()[0][3]} resulted in an empty update_dict')
#
#     return stmt.on_conflict_do_update(
#         index_elements=update_dict,
#         set_=update_dict,
#     )

# @api.post('/customers/{id}', response_model=Customer)
def upsert_value(session, result, model_create):
    """Upsert a value.

    It is used to create a value in the database if it does not already exist,
    else it is used to update the existing one.

    Args:
      session:
        with Session(engine) as session: ...
      result:
        The model data.
      model_create:
        The model input data.

    Returns:
      The upserted model.
    """

    # check if the device exists
    # statement = select(model).where(model.dict[column] == value)
    # result = await session.exec(statement).first()

    # if not, create it
    if result is None:
        result = model_create

    # sync the data
    for k, v in model_create.dict(exclude_unset=True).items():
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
        print(tag1)

        customer1 = Customer.from_orm(
            CustomerCreate(phone='79251234567'),
            update={
                'phone_code_id': phone_code1.id,
                'timezone_id': timezone.id,
            }
        )
        customer1.tags.append(tag1)

        session.add(customer1)
        session.commit()
        session.refresh(customer1)

        print(customer1)
        print(customer1.tags)
        # phone_code2 = await upsert_value(session, PhoneCode, PhoneCodeInput, 'phone_code', 935)
        #
        # # timezone = TimezoneInput(timezone='Europe/Moscow')
        # timezone = await upsert_value(session, Timezone, TimezoneInput, 'timezone', 'Europe/Moscow')
        #
        # # ctag1 = TagInput(tag='Female')
        # # ctag2 = TagInput(tag='Mother')
        # # ctag3 = TagInput(tag='Worker')
        # # ctag4 = TagInput(tag='Male')
        # # ctag5 = TagInput(tag='Student')
        # ctag1 = await upsert_value(session, Tag, TagInput, 'tag', 'Female')
        # ctag2 = await upsert_value(session, Tag, TagInput, 'tag', 'Mother')
        # ctag3 = await upsert_value(session, Tag, TagInput, 'tag', 'Worker')
        # ctag4 = await upsert_value(session, Tag, TagInput, 'tag', 'Male')
        # ctag5 = await upsert_value(session, Tag, TagInput, 'tag', 'Student')
        #
        # # mtag1 = TagInput(tag='Female')
        # # mtag2 = TagInput(tag='Male')
        # # mtag3 = TagInput(tag='Student')
        # mtag1 = await upsert_value(session, Tag, TagInput, 'tag', 'Female')
        # mtag2 = await upsert_value(session, Tag, TagInput, 'tag', 'Male')
        # mtag3 = await upsert_value(session, Tag, TagInput, 'tag', 'Student')
        #
        # # message1 = MessageInput(text_message='Test message 1')
        # # message2 = MessageInput(text_message='Test message 2')
        # message1 = await upsert_value(session, Message, MessageInput, 'text_message', 'Test message 1')
        # message2 = await upsert_value(session, Message, MessageInput, 'text_message', 'Test message 2')
        #
        # # await session.execute(insert_or_update(PhoneCode, {phone_code1, phone_code2}))
        # # await session.execute(insert_or_update(Timezone, {timezone}))
        # # await session.execute(insert_or_update(Tag, {ctag1, ctag2, ctag3, ctag4, ctag5, mtag1, mtag2, mtag3}))
        # # await session.execute(insert_or_update(Message, {message1, message2}))
        #
        # # await session.flush()
        # # await session.commit()
        #
        # # phone1 = CustomerInput(phone='79251234567')
        # # phone2 = CustomerInput(phone='79351234588')
        #
        # customer1 = Customer.from_orm(
        #     CustomerInput(phone='79251234567'),
        #     update={
        #         'phone_code': phone_code1,
        #         'timezone': timezone,
        #         'tags': list({ctag1, ctag2, ctag3})
        #     }
        # )
        #
        # customer2 = Customer.from_orm(
        #     CustomerInput(phone='79351234588'),
        #     update={
        #         'phone_code': phone_code2,
        #         'timezone': timezone,
        #         'tags': list({ctag4, ctag5})
        #     }
        # )
        #
        # await session.add(customer1)
        # await session.add(customer2)
        # await session.commit()
        # await session.refresh(customer1)
        # await session.refresh(customer2)
        #
        # print(f'Customer 1: {customer1}')
        # print(f'Customer 2: {customer2}')
        #
        # mailout = Mailout.from_orm(
        #     MailoutInput(
        #         start_time=datetime(2023, 6, 12, 10, 30),
        #         finish_time=datetime(2023, 6, 15, 10, 30),
        #         available_start=time(10, 30, 0),
        #         available_finish=time(19, 30, 0),
        #     ), update={
        #         'tags': list({mtag1, mtag2, mtag3}),
        #         'customers': list({customer1, customer2}),
        #         'phone_codes': list({phone_code1, phone_code2}),
        #         'messages': list({message1, message2}),
        #     }
        # )
        #
        # await session.add(mailout)
        # await session.commit()
        # await session.refresh(mailout)
        # print(f'Mailout: {mailout}')
