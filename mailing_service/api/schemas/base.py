from datetime import datetime

from sqlalchemy import Enum, text
from sqlmodel import Field, SQLModel


class StatusEnum(str, Enum):
    created = 'created'
    sent = 'sent'
    updated = 'updated'
    deleted = 'deleted'


class TimeStampModel(SQLModel):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={'server_default': text('current_timestamp(0)')},
    )
