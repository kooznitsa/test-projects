from typing import Optional, TYPE_CHECKING

from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship

from .base_class import StatusEnum

if TYPE_CHECKING:
    from .messages import Message


class StatusBase(SQLModel):
    status: StatusEnum


class Status(StatusBase, table=True):
    __tablename__: str = 'statuses'
    __table_args__ = (UniqueConstraint('status'),)

    id: int | None = Field(primary_key=True, default=None)

    messages: list['Message'] = Relationship(back_populates='status')


class StatusCreate(StatusBase):
    pass

    def __hash__(self):
        return hash(self.status)


class StatusRead(StatusBase):
    id: int


class StatusUpdate(SQLModel):
    status: Optional[StatusEnum] = None
