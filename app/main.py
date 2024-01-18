import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient

from api.v1 import likes, reviews, bookmarks
from db import databases
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    databases.mongo_client = AsyncIOMotorClient(
        f'mongodb://{settings.MONGODB_HOSTS}'
    )
    yield
    databases.mongo_client.close()


app = FastAPI(
    description='UGC сервис',
    version='0.0.0',
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=JSONResponse,
    lifespan=lifespan,
)


app.include_router(likes.router, prefix='/api/v1/likes', tags=['likes'])
app.include_router(reviews.router, prefix='/api/v1/reviews', tags=['reviews'])
app.include_router(bookmarks.router, prefix='/api/v1/bookmarks', tags=['bookmarks'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app', host='0.0.0.0', port=8000, reload=True
    )
