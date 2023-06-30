from datetime import datetime, time
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

from .phone_codes import PhoneCodeRead
from .tags import TagRead
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

    class Config:
        schema_extra = {
            "example": {
                "start_time": datetime(2023, 6, 30, 10, 0, 0),
                "finish_time": datetime(2023, 6, 30, 11, 0, 0),
                "available_start": time(10, 0, 0),
                "available_finish": time(19, 0, 0)
            }
        }


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
    phone_codes: list[PhoneCodeRead] = []
    tags: list[TagRead] = []


class MailoutUpdate(SQLModel):
    start_time: datetime | None = None
    finish_time: datetime | None = None
    available_start: time | None = None
    available_finish: time | None = None
