from fastapi import FastAPI, status
from sqlmodel import SQLModel, Session

from db.config import settings
from db.sample_data import add_sample_data
from db.sessions import engine
from routers import phone_codes, timezones, tags, customers, mailouts, messages

app = FastAPI(
    title=settings.title,
    version=settings.version,
    description=settings.description,
    openapi_prefix=settings.openapi_prefix,
    docs_url=settings.docs_url,
    openapi_url=settings.openapi_url,
)

routers = (
    (phone_codes.router, 'Phone Codes'),
    (timezones.router, 'Timezones'),
    (tags.router, 'Tags'),
    (customers.router, 'Customers'),
    (mailouts.router, 'Mailouts'),
    (messages.router, 'Messages'),
)

for router, tags in routers:
    app.include_router(router, prefix=settings.api_prefix, tags=[tags])


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
