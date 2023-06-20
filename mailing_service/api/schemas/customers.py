from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

from .link_schemas import CustomerTag
from .tags import TagRead

if TYPE_CHECKING:
    from .phone_codes import PhoneCode
    from .timezones import Timezone
    from .tags import Tag, TagRead


class CustomerBase(SQLModel):
    phone: str
    phone_code_id: int | None = Field(default=None, foreign_key='phone_codes.id')
    timezone_id: int | None = Field(default=1, foreign_key='timezones.id')

    class Config:
        schema_extra = {
            "example": {
                "phone": "79251234567",
                "phone_code_id": 1,
                "timezone_id": 1
            }
        }


class Customer(CustomerBase, table=True):
    __tablename__: str = 'customers'

    id: int | None = Field(primary_key=True, default=None)

    phone_code: Optional['PhoneCode'] = Relationship(back_populates='customers')
    timezone: Optional['Timezone'] = Relationship(back_populates='customers')
    tags: list['Tag'] = Relationship(back_populates='customers', link_model=CustomerTag)


class CustomerCreate(CustomerBase):
    pass


class CustomerRead(CustomerBase):
    id: int
    tags: list['TagRead'] = []


class CustomerUpdate(SQLModel):
    phone: str | None = None
    phone_code_id: int | None = None
    timezone_id: int | None = None
