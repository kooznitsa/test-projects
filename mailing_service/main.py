from fastapi import FastAPI, status
from sqlmodel import SQLModel

from api.routers import customers
from db.config import settings
from db.sessions import engine

app = FastAPI(
    title=settings.title,
    version=settings.version,
    description=settings.description,
    openapi_prefix=settings.openapi_prefix,
    docs_url=settings.docs_url,
    openapi_url=settings.openapi_url,
)

app.include_router(customers.router, prefix=settings.api_prefix)


@app.on_event('startup')
def init_tables():
    # SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


@app.get('/')
async def root():
    return {'Say': 'Hello!'}


if __name__ == '__main__':
    init_tables()
