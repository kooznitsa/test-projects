from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

import api.schemas as schemas


class CustomerInput(SQLModel):
    phone: str

    class Config:
        schema_extra = {
            "example": {
                "phone": "79251234567",
                "phone_code": 925,
                "timezone": "Europe/Moscow"
            }
        }


class CustomerOutput(CustomerInput):
    id: int
    phone_code: int | None
    timezone: Optional[str] = 'Europe/Moscow'
    tags: list['Tag'] = []
    mailouts: list['Mailout'] = []


class Customer(CustomerInput, table=True):
    __tablename__: str = 'customers'
    id: int | None = Field(primary_key=True, default=None)
    phone_code_id: int | None = Field(default=None, foreign_key='phone_codes.id')
    phone_code: Optional['PhoneCode'] = Relationship(
        back_populates='customers',
    )
    timezone_id: int = Field(default=1, foreign_key='timezones.id')
    timezone: Optional['Timezone'] = Relationship(
        back_populates='customers',
    )
    tags: list['Tag'] = Relationship(
        back_populates='customers',
        link_model=schemas.link_schemas.CustomerTag
    )
    mailouts: list['Mailout'] = Relationship(
        back_populates='customers',
        link_model=schemas.link_schemas.MailoutCustomer
    )


from .phone_codes import PhoneCode
from .timezones import Timezone
from .tags import Tag
from .mailouts import Mailout

CustomerOutput.update_forward_refs()
