from fastapi import FastAPI, status

from api.routers import customers
from db.config import settings
from db.sessions import create_tables_from_models

app = FastAPI(
    title=settings.title,
    version=settings.version,
    description=settings.description,
    openapi_prefix=settings.openapi_prefix,
    docs_url=settings.docs_url,
    openapi_url=settings.openapi_url,
)

app.include_router(customers.router, prefix=settings.api_prefix)


# @app.get('/init_tables', status_code=status.HTTP_200_OK, name='init_tables')
@app.on_event('startup')
async def init_tables():
    await create_tables_from_models()


@app.get('/')
async def root():
    return {'Say': 'Hello!'}