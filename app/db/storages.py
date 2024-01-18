from typing import Any, Annotated
from abc import ABC, abstractmethod

from fastapi import Depends

from motor.motor_asyncio import AsyncIOMotorClient
from .databases import get_mongo_client
from core.config import settings


class IStorage(ABC):
	@abstractmethod
	async def find_element_by_properties(
		self, properties: dict, collection_name: str
	) -> Any:
		pass

	@abstractmethod
	async def find_elements_by_properties(
		self, properties: dict, collection_name: str
	) -> list[Any]:
		pass

	@abstractmethod
	async def insert_element(
		self, element: dict, collection_name: str
	) -> None:
		pass

	@abstractmethod
	async def delete_element(
		self, element: dict, collection_name: str
	) -> None:
		pass


class MongoStorage(IStorage):
	def __init__(
		self,
		client: AsyncIOMotorClient,
		database_name: str
	):
		self.database_client = client[database_name]

	async def find_element_by_properties(
		self, properties: dict, collection_name: str
	) -> Any:
		return await self.database_client[collection_name].find_one(properties)

	async def find_elements_by_properties(
		self, properties: dict, collection_name: str
	) -> list[Any]:
		return await self.database_client[
			collection_name
		].find(properties).to_list(length=None)

	async def insert_element(
		self, element: dict, collection_name: str
	) -> None:
		await self.database_client[collection_name].insert_one(element)

	async def delete_element(
		self, element: dict, collection_name: str
	) -> None:
		await self.database_client[collection_name].delete_one(element)


def get_storage(
	client: Annotated[AsyncIOMotorClient, Depends(get_mongo_client)]
) -> IStorage:
	return MongoStorage(client, settings.MONGO_DATABASE_NAME)
