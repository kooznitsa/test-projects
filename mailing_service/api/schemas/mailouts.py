from datetime import datetime, time
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

from .link_schemas import MailoutPhoneCode, MailoutTag

if TYPE_CHECKING:
    from .phone_codes import PhoneCode, PhoneCodeRead
    from .tags import Tag, TagRead
    from .messages import Message


class MailoutBase(SQLModel):
    start_time: datetime
    finish_time: datetime
    available_start: time | None = None
    available_finish: time | None = None


class Mailout(MailoutBase, table=True):
    __tablename__: str = 'mailouts'

    id: int | None = Field(primary_key=True, default=None)
    tags: list['Tag'] = Relationship(back_populates='mailouts', link_model=MailoutTag)
    phone_codes: list['PhoneCode'] = Relationship(back_populates='mailouts', link_model=MailoutPhoneCode)
    messages: list['Message'] = Relationship(back_populates='mailout')


class MailoutCreate(MailoutBase):
    pass


class MailoutRead(MailoutBase):
    id: int
    phones_codes: list['PhoneCodeRead'] = []
    tags: list['TagRead'] = []
