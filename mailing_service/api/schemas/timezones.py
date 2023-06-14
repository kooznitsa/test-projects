from sqlmodel import SQLModel, Field, Relationship


class TimezoneInput(SQLModel):
    timezone: str


class TimezoneOutput(TimezoneInput):
    id: int


class Timezone(TimezoneInput, table=True):
    __tablename__: str = 'timezones'
    id: int | None = Field(default=None, primary_key=True)
    customers: 'Customer' = Relationship(back_populates='timezone')
