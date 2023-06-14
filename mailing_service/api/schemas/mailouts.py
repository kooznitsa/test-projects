from datetime import datetime, time

from sqlmodel import SQLModel, Field, Relationship

import api.schemas as schemas


class MailoutInput(SQLModel):
    start_time: datetime
    finish_time: datetime
    available_start: time | None = None
    available_finish: time | None = None


class MailoutOutput(MailoutInput):
    id: int
    customers: list['Customer'] = []
    messages: list['Message'] = []
    phones_codes: list['PhoneCode'] = []
    tags: list['Tag'] = []


class Mailout(MailoutInput, table=True):
    __tablename__: str = 'mailouts'
    id: int | None = Field(primary_key=True, default=None)
    customers: list['Customer'] = Relationship(
        back_populates='mailouts', link_model=schemas.link_schemas.MailoutCustomer
    )
    messages: list['Message'] = Relationship(back_populates='mailout')
    phone_codes: list[schemas.phone_codes.PhoneCode] = Relationship(
        back_populates='mailouts', link_model=schemas.link_schemas.MailoutPhoneCode
    )
    tags: list['Tag'] = Relationship(
        back_populates='mailouts', link_model=schemas.link_schemas.MailoutTag
    )
