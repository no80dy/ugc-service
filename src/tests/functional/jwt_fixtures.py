import pytest_asyncio

from schemas.entity import UGCPayloads, FilmLikePayloads, FilmCommentPayloads, FilmFavoritePayloads
from .utils.generate_jwt import generated_token


@pytest_asyncio.fixture(scope='function')
async def create_fake_jwt():
    async def inner(user_id: str) -> dict:
        generated_token(user_id)

        return generated_token(user_id)

    return inner


@pytest_asyncio.fixture(scope='function')
async def create_fake_film_like(
        create_fake_event
):
    async def inner() -> dict:
        fake_film_like = FilmLikePayloads(
            collection_name="events_ugc",
            user_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
            film_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
            created_at="2024-01-24T12:09:56.434178",
            event_name="film_likes",
            score=0
        )
        await create_fake_event(fake_film_like)
    return inner
