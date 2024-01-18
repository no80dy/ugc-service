from uuid import UUID
from typing import Annotated
from functools import lru_cache
from fastapi import Depends

from db.storages import IStorage, get_storage
from schemas.bookmarks import BookmarkResponseSchema
from core.config import settings


class BookmarkService:
	def __init__(
		self, storage: IStorage
	):
		self.storage = storage

	async def _is_movie_exists(
		self, movie_id: UUID
	) -> bool:
		return await self.storage.find_element_by_properties(
			{'_id': str(movie_id)}, settings.MONGO_MOVIE_COLLECTION
		)

	async def get_user_bookmarks(
		self, user_id: UUID
	) -> list[BookmarkResponseSchema]:
		bookmarks = await self.storage.find_elements_by_properties(
			{"userId": user_id}, settings.MONGO_BOOKMARK_COLLECTION
		)
		return [
			BookmarkResponseSchema(
				user_id=bookmark['userId'], movie_id=bookmark['movieId'],
			)
			for bookmark in bookmarks
		]

	async def add_movie_in_bookmark(
		self, user_id: UUID, movie_id: UUID
	) -> BookmarkResponseSchema | None:
		if await self.storage.find_element_by_properties(
			{
				'userId': str(user_id), 'movieId': str(movie_id)
			},
			settings.MONGO_BOOKMARK_COLLECTION
		):
			return None

		await self.storage.insert_element(
			{
				'userId': str(user_id), 'movieId': str(movie_id)
			},
			settings.MONGO_BOOKMARK_COLLECTION
		)
		return BookmarkResponseSchema(user_id=user_id, movie_id=movie_id)

	async def delete_user_bookmark(
		self, user_id: UUID, movie_id: UUID
	) -> BookmarkResponseSchema | None:
		if not await self._is_movie_exists(movie_id):
			return None

		await self.storage.delete_element(
			{
				'userId': str(user_id), 'movieId': str(movie_id),
			},
			settings.MONGO_BOOKMARK_COLLECTION
		)
		return BookmarkResponseSchema(user_id=user_id, movie_id=movie_id)


@lru_cache()
def get_bookmark_service(
	storage: Annotated[IStorage, Depends(get_storage)]
) -> BookmarkService:
	return BookmarkService(storage)
