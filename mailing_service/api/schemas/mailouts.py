from datetime import datetime, time

from sqlmodel import SQLModel, Field, Relationship

from schemas.customers import Customer, CustomerOutput
from schemas.messages import Message, MessageOutput
from schemas.phone_codes import PhoneCode, PhoneCodeOutput
from schemas.tags import Tag, TagOutput


class MailoutTag(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    mailout_id: int | None = Field(
        default=None, foreign_key='mailout.id', primary_key=True
    )
    tag_id: int | None = Field(
        default=None, foreign_key='tag.id', primary_key=True
    )


class MailoutPhoneCode(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    mailout_id: int | None = Field(
        default=None, foreign_key='mailout.id', primary_key=True
    )
    phone_code_id: int | None = Field(
        default=None, foreign_key='phone_code.id', primary_key=True
    )


class MailoutCustomer(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    mailout_id: int | None = Field(
        default=None, foreign_key='mailout.id', primary_key=True
    )
    customer_id: int | None = Field(
        default=None, foreign_key='customer.id', primary_key=True
    )


class MailoutInput(SQLModel):
    start_time: datetime
    finish_time: datetime
    available_start: time | None = None
    available_finish: time | None = None


class MailoutOutput(MailoutInput):
    id: int
    customers: list[CustomerOutput] = []
    messages: list[MessageOutput] = []
    phones_codes: list[PhoneCodeOutput] = []
    tags: list[TagOutput] = []


class Mailout(MailoutInput, table=True):
    id: int | None = Field(primary_key=True, default=None)
    
    customers: list[Customer] = Relationship(back_populates='mailouts', link_model=MailoutCustomer)
    messages: list[Message] = Relationship(back_populates='mailout')
    phone_codes: list[PhoneCode] = Relationship(back_populates='mailouts', link_model=MailoutPhoneCode)
    tags: list[Tag] = Relationship(back_populates='mailouts', link_model=MailoutTag)