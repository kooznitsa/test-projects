from datetime import datetime

from sqlalchemy import text
from sqlmodel import SQLModel, Field, Relationship


class StatusInput(SQLModel):
    status: str


class StatusOutput(StatusInput):
    id: int


class Status(StatusInput, table=True):
    id: int | None = Field(primary_key=True, default=None)
    status: str = Relationship(back_populates='message')


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