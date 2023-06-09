from sqlmodel import SQLModel, Field, Relationship

from schemas.customers import Customer
from schemas.mailouts import Mailout, MailoutPhoneCode


class PhoneCodeInput(SQLModel):
    phone_code: int


class PhoneCodeOutput(PhoneCodeInput):
    id: int


class PhoneCode(PhoneCodeInput, table=True):
    id: int | None = Field(default=None, primary_key=True)

    customer: Customer | None = Relationship(back_populates='phone_code')
    mailouts: list[Mailout] = Relationship(back_populates='phone_codes', link_model=MailoutPhoneCode)