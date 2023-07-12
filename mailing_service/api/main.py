from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session
from starlette.responses import JSONResponse
from starlette import status

from db.config import settings
from db.errors import PhoneLengthError, TimezoneError
from db.sample_data import add_sample_data
from db.sessions import engine
from routers import auth, phone_codes, timezones, tags, customers, mailouts, messages, web

app = FastAPI(
    title=settings.title,
    version=settings.version,
    description=settings.description,
    openapi_prefix=settings.openapi_prefix,
    docs_url=settings.docs_url,
    openapi_url=settings.openapi_url,
)

app.include_router(auth.router, tags=['Authentication'])

routers = (
    (phone_codes.router, 'Phone Codes'),
    (timezones.router, 'Timezones'),
    (tags.router, 'Tags'),
    (customers.router, 'Customers'),
    (mailouts.router, 'Mailouts'),
    (messages.router, 'Messages'),
    (web.router, 'Web'),
)

for router, tags in routers:
    app.include_router(router, prefix=settings.api_prefix, tags=[tags])

origins = [
    'http://localhost:8000',
    'http://localhost:8080',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event('startup')
async def init_tables():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    add_sample_data()


@app.exception_handler(PhoneLengthError)
async def phone_length_exception_handler(request: Request, exc: PhoneLengthError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={'message': 'Phone length is not equal to 7 digits'},
    )


@app.exception_handler(TimezoneError)
async def timezone_exception_handler(request: Request, exc: TimezoneError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={'message': 'Timezone is not in the list of timezones'},
    )


@app.get('/')
async def root():
    return {'Say': 'Hello!'}


if __name__ == '__main__':
    init_tables()
