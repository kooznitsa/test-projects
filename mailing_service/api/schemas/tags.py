from sqlmodel import SQLModel, Field, Relationship

import api.schemas as schemas


class TagInput(SQLModel):
    tag: str


class TagOutput(TagInput):
    id: int


class Tag(TagInput, table=True):
    __tablename__: str = 'tags'
    id: int | None = Field(default=None, primary_key=True)
    customers: list['Customer'] = Relationship(
        back_populates='tags',
        link_model=schemas.link_schemas.CustomerTag
    )
    mailouts: list['Mailout'] = Relationship(
        back_populates='tags',
        link_model=schemas.link_schemas.MailoutTag
    )
