from datetime import datetime, time
from typing import Optional

from sqlalchemy import text
from sqlmodel import SQLModel, Field, Relationship


class CustomerTag(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    customer_id: int | None = Field(
        default=None, foreign_key='customer.id', primary_key=True
    )
    tag_id: int | None = Field(
        default=None, foreign_key='tag.id', primary_key=True
    )


class MailoutTag(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    mailout_id: int | None = Field(
        default=None, foreign_key='mailout.id', primary_key=True
    )
    tag_id: int | None = Field(
        default=None, foreign_key='tag.id', primary_key=True
    )


class MailoutCustomer(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    mailout_id: int | None = Field(
        default=None, foreign_key='mailout.id', primary_key=True
    )
    customer_id: int | None = Field(
        default=None, foreign_key='customer.id', primary_key=True
    )


class MailoutPhoneCode(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    mailout_id: int | None = Field(
        default=None, foreign_key='mailout.id', primary_key=True
    )
    phone_code_id: int | None = Field(
        default=None, foreign_key='phonecode.id', primary_key=True
    )


class PhoneCodeInput(SQLModel):
    phone_code: int


class PhoneCodeOutput(PhoneCodeInput):
    id: int


class PhoneCode(PhoneCodeInput, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customers: list['Customer'] = Relationship(back_populates='phone_code')
    mailouts: list['Mailout'] = Relationship(
        back_populates='phone_codes', link_model=MailoutPhoneCode
    )


class TimezoneInput(SQLModel):
    timezone: str


class TimezoneOutput(TimezoneInput):
    id: int


class Timezone(TimezoneInput, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customers: 'Customer' = Relationship(back_populates='timezone')


class TagInput(SQLModel):
    tag: str


class TagOutput(TagInput):
    id: int


class Tag(TagInput, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customers: list['Customer'] = Relationship(back_populates='tags', link_model=CustomerTag)
    mailouts: list['Mailout'] = Relationship(back_populates='tags', link_model=MailoutTag)


class StatusInput(SQLModel):
    status: str


class StatusOutput(StatusInput):
    id: int


class Status(StatusInput, table=True):
    id: int | None = Field(primary_key=True, default=None)
    messages: list['Message'] = Relationship(back_populates='status')


class MessageInput(SQLModel):
    text_message: str
    create_date: datetime


class MessageOutput(MessageInput):
    id: int


class Message(MessageInput, table=True):
    id: int | None = Field(primary_key=True, default=None)
    created_date: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={'server_default': text('current_timestamp(0)')},
    )
    status_id: int = Field(foreign_key='status.id')
    mailout_id: int = Field(foreign_key='mailout.id')
    status: 'Status' = Relationship(back_populates='messages')
    mailout: 'Mailout' = Relationship(back_populates='messages')


class CustomerInput(SQLModel):
    phone: str

    class Config:
        schema_extra = {
            "example": {
                "phone": "79251234567",
                "phone_code": 925,
                "timezone": "Europe/Moscow"
            }
        }


class CustomerOutput(CustomerInput):
    id: int
    phone_code: int
    timezone: str
    tags: list = []


class Customer(CustomerInput, table=True):
    id: int | None = Field(primary_key=True, default=None)
    phone_code_id: int | None = Field(default=None, foreign_key='phonecode.id')
    timezone_id: int = Field(default=1, foreign_key='timezone.id')
    phone_code: Optional[PhoneCode] = Relationship(back_populates='customers')
    timezone: Optional[Timezone] = Relationship(back_populates='customers')
    tags: list['Tag'] = Relationship(back_populates='customers', link_model=CustomerTag)
    mailouts: list['Mailout'] = Relationship(back_populates='customers', link_model=MailoutCustomer)


class MailoutInput(SQLModel):
    start_time: datetime
    finish_time: datetime
    available_start: time | None = None
    available_finish: time | None = None


class MailoutOutput(MailoutInput):
    id: int
    customers: list[Customer] = []
    messages: list[Message] = []
    phones_codes: list[PhoneCode] = []
    tags: list[Tag] = []


class Mailout(MailoutInput, table=True):
    id: int | None = Field(primary_key=True, default=None)
    customers: list[Customer] = Relationship(back_populates='mailouts', link_model=MailoutCustomer)
    messages: list[Message] = Relationship(back_populates='mailout')
    phone_codes: list[PhoneCode] = Relationship(back_populates='mailouts', link_model=MailoutPhoneCode)
    tags: list[Tag] = Relationship(back_populates='mailouts', link_model=MailoutTag)
