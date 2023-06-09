from sqlmodel import SQLModel, Field, Relationship

from api.schemas.customers import CustomerTag
from api.schemas.mailouts import MailoutTag


class TagInput(SQLModel):
    tag: str


class TagOutput(TagInput):
    id: int


class Tag(TagInput, table=True):
    id: int | None = Field(default=None, primary_key=True)

    customers: list['Customer'] = Relationship(back_populates='tags', link_model=CustomerTag)
    mailouts: list['Mailout'] = Relationship(back_populates='tags', link_model=MailoutTag)