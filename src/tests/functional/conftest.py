import asyncio
import logging

import pytest
import pytest_asyncio

from motor.motor_asyncio import AsyncIOMotorClient

from .settings import test_settings


@pytest.fixture(scope="session")
def event_loop():
	try:
		loop = asyncio.get_running_loop()
	except RuntimeError:
		loop = asyncio.new_event_loop()
	yield loop
	loop.close()


@pytest_asyncio.fixture(scope='session')
async def mongo_client() -> AsyncIOMotorClient:
	try:
		client = AsyncIOMotorClient(host=test_settings.mongodb_url)
	except ConnectionError as e:
		logging.error(e)
	yield client
	client.close()


pytest_plugins = [
	'tests.functional.api_fixtures',
	'tests.functional.mongo_fixtures',
	'tests.functional.jwt_fixtures',
]
