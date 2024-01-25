import pytest_asyncio

from tests.functional.utils.generate_jwt import generate_token


@pytest_asyncio.fixture(scope='function')
async def create_fake_jwt():
    async def inner(user_id: str) -> dict:
        return generate_token(user_id)
    return inner
