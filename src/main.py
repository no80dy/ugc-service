import structlog
import uvicorn

from http import HTTPStatus
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from logging import config as logging_config

from api.v1 import events
from core.config import settings
from db import storage
from db.mongodb import MongoStorage
from core.logger import LOGGING


logging_config.dictConfig(LOGGING)

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.format_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    logger_factory=structlog.stdlib.LoggerFactory()
)

logger = structlog.get_logger()


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
    title=settings.project_name,
    docs_url='/ugc/api/openapi',
    openapi_url='/ugc/api/openapi.json',
    default_response_class=JSONResponse,
    lifespan=lifespan,
)


@app.middleware('http')
async def check_request_id(request: Request, call_next):
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content='X-Request-Id is missing'
        )
    structlog.contextvars.bind_contextvars(request_id=request_id)
    return await call_next(request)


@app.get('/check')
async def check() -> dict:
    logger.info('сhecked')

    return {'is_checked': True}


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
