from fastapi import FastAPI, status
from sqlmodel import SQLModel, Session

from db.config import settings
from db.sample_data import add_sample_data
from db.sessions import engine
from routers import phone_codes, timezones, customers

app = FastAPI(
    title=settings.title,
    version=settings.version,
    description=settings.description,
    openapi_prefix=settings.openapi_prefix,
    docs_url=settings.docs_url,
    openapi_url=settings.openapi_url,
)

app.include_router(phone_codes.router, prefix=settings.api_prefix, tags=['Phone Codes'])
app.include_router(timezones.router, prefix=settings.api_prefix, tags=['Timezones'])
app.include_router(customers.router, prefix=settings.api_prefix, tags=['Customers'])


@app.on_event('startup')
async def init_tables():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    add_sample_data()


@app.get('/')
async def root():
    return {'Say': 'Hello!'}


if __name__ == '__main__':
    init_tables()
