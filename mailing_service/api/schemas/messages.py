from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

from .base import StatusEnum, TimeStampModel

if TYPE_CHECKING:
    from .mailouts import Mailout
    from .customers import Customer


class MessageBase(SQLModel):
    text_message: str
    mailout_id: int | None = Field(default=None, foreign_key='mailouts.id')
    customer_id: int | None = Field(default=None, foreign_key='customers.id')

    class Config:
        schema_extra = {
            "example": {
                "text_message": "Test message",
                "mailout_id": 1,
                "customer_id": 1
            }
        }


class Message(MessageBase, TimeStampModel, table=True):
    __tablename__: str = 'messages'

    id: int | None = Field(primary_key=True, default=None)
    status: StatusEnum = StatusEnum.created

    mailout: 'Mailout' = Relationship(back_populates='messages')
    customer: 'Customer' = Relationship(back_populates='messages')


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase, TimeStampModel):
    id: int
    status: str


class MessageUpdate(SQLModel):
    text_message: Optional[str]
    mailout_id: int | None = None
    customer_id: int | None = None
