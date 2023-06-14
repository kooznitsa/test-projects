from datetime import datetime, time

from sqlmodel import Session

import api.schemas as schemas
from db.sessions import engine


def add_sample_data():
    with Session(engine) as session:
        phone_code1 = schemas.phone_codes.PhoneCode(phone_code=925)
        phone_code2 = schemas.phone_codes.PhoneCode(phone_code=935)

        timezone = schemas.timezones.Timezone(timezone='Europe/Moscow')

        ctag1 = schemas.tags.Tag(tag='Female')
        ctag2 = schemas.tags.Tag(tag='Mother')
        ctag3 = schemas.tags.Tag(tag='Worker')
        ctag4 = schemas.tags.Tag(tag='Male')
        ctag5 = schemas.tags.Tag(tag='Student')

        mtag1 = schemas.tags.Tag(tag='Female')
        mtag2 = schemas.tags.Tag(tag='Male')
        mtag3 = schemas.tags.Tag(tag='Student')

        status = schemas.statuses.Status(status='Created')

        message1 = schemas.messages.Message(
            text_message='Test message 1',
            status=status,
        )
        message2 = schemas.messages.Message(
            text_message='Test message 2',
            status=status,
        )

        customer1 = schemas.customers.Customer(
            phone='79251234567',
            phone_code=phone_code1,
            timezone=timezone,
            tags=[ctag1, ctag2, ctag3],
        )
        customer2 = schemas.customers.Customer(
            phone='79351234588',
            phone_code=phone_code2,
            timezone=timezone,
            tags=[ctag4, ctag5],
        )

        mailout = schemas.mailouts.Mailout(
            start_time=datetime(2023, 6, 12, 10, 30),
            finish_time=datetime(2023, 6, 15, 10, 30),
            available_start=time(10, 30, 0),
            available_finish=time(19, 30, 0),
            tags=[mtag1, mtag2, mtag3],
            customers=[customer1, customer2],
            phones_codes=[phone_code1, phone_code2],
            messages=[message1, message2],
        )

        entities = (
            phone_code1, phone_code2, timezone, ctag1, ctag2, ctag3, ctag4, ctag5,
            mtag1, mtag2, mtag3, status, message1, message2, customer1, customer2,
            mailout,
        )

        for entity in entities:
            session.add(entity)

        session.commit()

        for entity in entities:
            session.refresh(entity)

        print(f'Mailout added: {mailout}')
