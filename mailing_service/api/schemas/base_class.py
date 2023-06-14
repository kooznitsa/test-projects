from datetime import datetime

from sqlalchemy import Enum, text
from sqlmodel import Field, SQLModel


class StatusEnum(str, Enum):
    active: 'active'
    inactive: 'inactive'
    deleted: 'deleted'


class TimeStampModel(SQLModel):
    created_date: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={'server_default': text('current_timestamp(0)')},
    )
