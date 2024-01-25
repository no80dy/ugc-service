import asyncio
import logging
import pytest
import pytest_asyncio

from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.encoders import jsonable_encoder

from schemas.entity import UGCPayloads, FilmLikePayloads, FilmCommentPayloads, FilmFavoritePayloads
from .settings import test_settings


@pytest_asyncio.fixture(scope='session')
async def mongo_client() -> AsyncIOMotorClient:
    async with AsyncIOMotorClient(host=test_settings.mongodb_url) as client:
        yield client


@pytest_asyncio.fixture(scope='function')
async def create_fake_event(client: AsyncIOMotorClient):
    async def inner(fake_event: UGCPayloads) -> None:
        event_dto = jsonable_encoder(fake_event)
        db = client.connection.get_database(test_settings.database_name)
        collection = db.get_collection(event_dto.get('collection_name'))
        try:
            await collection.insert_one(
                fake_event.model_dump(
                    by_alias=True, exclude={'id', 'collection_name'}
                )
            )

        except Exception as e:
            logging.error(e)
    return inner


@pytest_asyncio.fixture(scope='function')
async def create_fake_film_like(
        create_fake_event
):
    async def inner() -> dict:
        fake_film_like = FilmLikePayloads(
            collection_name="events_ugc",
            user_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
            film_id="3fa85f64-5717-4562-b3fc-2c963f66afa8",
            created_at="2024-01-24T12:09:56.434178",
            event_name="film_likes",
            score=0
        )
        await create_fake_event(fake_film_like)
    return inner

@pytest_asyncio.fixture(scope='function')
async def create_fake_film_favorites(
        create_fake_event
):
    async def inner() -> dict:
        fake_film_favorites = [
            FilmFavoritePayloads(
                collection_name="events_ugc",
                user_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
                film_id="3fa85f64-5717-4562-b3fc-2c963f66afa4",
                created_at="2024-01-24T12:09:56.434178",
                event_name="film_favorites",
            ),
            FilmFavoritePayloads(
                collection_name="events_ugc",
                user_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
                film_id="3fa85f64-5717-4562-b3fc-2c963f66afa2",
                created_at="2024-01-24T12:09:56.434178",
                event_name="film_favorites",
            ),
        ]
        for fake_favorite in fake_film_favorites:
            await create_fake_event(fake_favorite)
    return inner