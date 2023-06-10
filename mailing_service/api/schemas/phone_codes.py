from sqlmodel import SQLModel, Field, Relationship

from api.schemas.mailouts import MailoutPhoneCode


class PhoneCodeInput(SQLModel):
    phone_code: int


class PhoneCodeOutput(PhoneCodeInput):
    id: int


class PhoneCode(PhoneCodeInput, table=True):
    id: int | None = Field(default=None, primary_key=True)

    customer: 'CustomerOutput' | None = Relationship(back_populates='phone_code')
    mailouts: list = Relationship(back_populates='phone_codes', link_model=MailoutPhoneCode)