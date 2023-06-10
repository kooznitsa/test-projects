from sqlmodel import SQLModel, Field, Relationship


class TimezoneInput(SQLModel):
    timezone: str


class TimezoneOutput(TimezoneInput):
    id: int


class Timezone(TimezoneInput, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer: 'CustomerOutput' = Relationship(back_populates='timezone')


class CustomerTag(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    customer_id: int | None = Field(
        default=None, foreign_key='customer.id', primary_key=True
    )
    tag_id: int | None = Field(
        default=None, foreign_key='tag.id', primary_key=True
    )


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
    """tags: list['Tag'] = []
    -> TypeError: issubclass() arg 1 must be a class
    The issue is the self-reference(children: List[CategoryModel]).
    Using just list or List[Any] avoids the error.
    """
    id: int
    phone_code: int
    timezone: str | None = 'Europe/Moscow'
    tags: list = []


class Customer(CustomerInput, table=True):
    id: int | None = Field(primary_key=True, default=None)
    phone_code_id: int = Field(foreign_key='phone_code.id')
    timezone_id: int = Field(default=None, foreign_key='timezone.id')
    tags: list = Relationship(back_populates='customers', link_model=CustomerTag)