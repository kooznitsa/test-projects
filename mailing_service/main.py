from fastapi import FastAPI, status

from api.routers import customers
from database.config import settings
from database.create_database import create_database

app = FastAPI(
    title=settings.title,
    version=settings.version,
    description=settings.description,
    openapi_prefix=settings.openapi_prefix,
    docs_url=settings.docs_url,
    openapi_url=settings.openapi_url,
)

app.include_router(customers.router, prefix=settings.api_prefix)


@app.get('/')
async def root():
    return {'Say': 'Hello!'}


@app.get('/init_tables', status_code=status.HTTP_200_OK, name='init_tables')
async def init_tables():
    create_database()