from sqlmodel import SQLModel, Field, Relationship

from schemas.customers import Customer, CustomerTag
from schemas.mailouts import Mailout, MailoutTag



class TagInput(SQLModel):
    tag: str


class TagOutput(TagInput):
    id: int


class Tag(TagInput, table=True):
    id: int | None = Field(default=None, primary_key=True)

    customers: list[Customer] = Relationship(back_populates='tags', link_model=CustomerTag)
    mailouts: list[Mailout] = Relationship(back_populates='tags', link_model=MailoutTag)