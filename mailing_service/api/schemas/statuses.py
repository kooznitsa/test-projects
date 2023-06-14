from sqlmodel import SQLModel, Field, Relationship

from api.schemas.base_class import StatusEnum


class StatusInput(SQLModel):
    status: StatusEnum


class StatusOutput(StatusInput):
    id: int


class Status(StatusInput, table=True):
    __tablename__: str = 'statuses'
    id: int | None = Field(primary_key=True, default=None)
    messages: list['Message'] = Relationship(back_populates='status')
