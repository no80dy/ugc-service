import asyncio
import logging
import pytest
import pytest_asyncio

from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.encoders import jsonable_encoder

from schemas.entity import UGCPayloads, FilmLikePayloads, FilmCommentPayloads, FilmFavoritePayloads
from tests.functional.settings import test_settings


@pytest.fixture(scope='session')
def mongo_client() -> AsyncIOMotorClient:
    try:
        client = AsyncIOMotorClient(host=test_settings.mongodb_url)
        yield client
        client.close()
    except ConnectionError as e:
        logging.error(e)


@pytest_asyncio.fixture(scope='function')
def create_fake_event(mongo_client: AsyncIOMotorClient):
    async def inner(fake_event: UGCPayloads) -> None:
        event_dto = jsonable_encoder(fake_event)
        db = mongo_client[test_settings.database_name]
        collection = db[event_dto.get('collection_name')]
        try:
            result = await collection.insert_one(
                fake_event.model_dump(
                    by_alias=True, exclude={'id', 'collection_name'}
                )
            )
            print(result)
        except Exception as e:
            logging.error(e)
    return inner


@pytest_asyncio.fixture(scope='function')
def create_fake_film_like(
    create_fake_event
):
    async def inner():
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
def create_fake_film_favorites(
    create_fake_event
):
    async def inner():
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


@pytest_asyncio.fixture(scope='function', autouse=True)
async def clean_collecion(mongo_client: AsyncIOMotorClient):
        await mongo_client['films_ugc']['events_ugc'].drop()
