from sqlmodel import SQLModel, Field, Relationship

import api.schemas as schemas


class PhoneCodeInput(SQLModel):
    phone_code: int


class PhoneCodeOutput(PhoneCodeInput):
    id: int


class PhoneCode(PhoneCodeInput, table=True):
    __tablename__: str = 'phone_codes'
    id: int | None = Field(default=None, primary_key=True)
    customers: list['Customer'] = Relationship(
        back_populates='phone_code',
    )
    mailouts: list['Mailout'] = Relationship(
        back_populates='phone_codes', link_model=schemas.link_schemas.MailoutPhoneCode
    )