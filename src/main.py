import uvicorn
from bson.binary import UuidRepresentation

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from api.v1 import events
from core.config import settings

from db import storage
from db.mongodb import MongoStorage


@asynccontextmanager
async def lifespan(app: FastAPI):
    storage.mongo = MongoStorage(
        host=settings.mongodb_url,
        UuidRepresentation='standard',
    )
    yield
    await storage.mongo.close()


app = FastAPI(
    description='Сервис сбора пользовательских данных о фильмах',
    version='1.0.0',
    # Конфигурируем название проекта. Оно будет отображаться в документации
    title=settings.project_name,
    # Адрес документации в красивом интерфейсе
    docs_url='/ugc/api/openapi',
    # Адрес документации в формате OpenAPI
    openapi_url='/ugc/api/openapi.json',
    default_response_class=JSONResponse,
    lifespan=lifespan,
)


app.include_router(events.router, prefix='/ugc/api/v1/statistic', tags=['statistic'])


if __name__ == '__main__':
    # Приложение может запускаться командой
    # `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True
    )
