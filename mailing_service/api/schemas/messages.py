from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

from .base_classes import TimeStampModel

if TYPE_CHECKING:
    from .statuses import Status
    from .mailouts import Mailout


class MessageBase(SQLModel):
    text_message: str
    status_id: int | None = Field(default=1, foreign_key='statuses.id')
    mailout_id: int | None = Field(default=None, foreign_key='mailouts.id')
    customer_id: int | None = Field(default=None, foreign_key='customers.id')


class Message(MessageBase, TimeStampModel, table=True):
    __tablename__: str = 'messages'

    id: int | None = Field(primary_key=True, default=None)

    status: 'Status' = Relationship(back_populates='messages')
    mailout: 'Mailout' = Relationship(back_populates='messages')


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase, TimeStampModel):
    id: int


class MessageUpdate(SQLModel):
    text_message: Optional[str]
    status_id: int | None = None
    mailout_id: int | None = None
    customer_id: int | None = None
