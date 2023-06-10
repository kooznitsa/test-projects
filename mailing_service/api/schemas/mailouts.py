from datetime import datetime, time

from sqlmodel import SQLModel, Field, Relationship


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
    customers: list = []
    messages: list = []
    phones_codes: list = []
    tags: list = []


class Mailout(MailoutInput, table=True):
    id: int | None = Field(primary_key=True, default=None)
    customers: list = Relationship(back_populates='mailouts', link_model=MailoutCustomer)
    messages: list = Relationship(back_populates='mailout')
    phone_codes: list = Relationship(back_populates='mailouts', link_model=MailoutPhoneCode)
    tags: list = Relationship(back_populates='mailouts', link_model=MailoutTag)