import pytest

from tests.functional.utils.generate_jwt import generate_token


@pytest.fixture(scope='function')
def create_fake_jwt():
    def inner(user_id: str) -> dict:
        return generate_token(user_id)
    return inner
