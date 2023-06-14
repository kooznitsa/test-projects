from datetime import datetime

from sqlalchemy import text
from sqlmodel import SQLModel, Field, Relationship

from api.schemas.base_class import TimeStampModel


class MessageInput(SQLModel):
    text_message: str


class MessageOutput(MessageInput):
    id: int


class Message(MessageInput, TimeStampModel, table=True):
    __tablename__: str = 'messages'
    id: int | None = Field(primary_key=True, default=None)
    status_id: int = Field(foreign_key='statuses.id')
    status: 'Status' = Relationship(back_populates='messages')
    mailout_id: int = Field(foreign_key='mailouts.id')
    mailout: 'Mailout' = Relationship(back_populates='messages')
