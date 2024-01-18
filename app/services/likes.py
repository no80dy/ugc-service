from uuid import UUID
from typing import Annotated
from functools import lru_cache
from fastapi import Depends

from db.storages import IStorage, get_storage
from schemas.likes import ScoreResponseSchema, DeleteScoreResponseSchema
from core.config import settings


class LikeService:
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

	async def add_like(
		self, user_id: UUID, movie_id: UUID, rank: int
	) -> ScoreResponseSchema | None:
		if not await self._is_movie_exists(movie_id):
			return None

		if await self.storage.find_element_by_properties(
			{
				'movieId': str(movie_id), 'userId': str(user_id)
			},
			settings.MONGO_LIKE_COLLECTION
		):
			return None

		await self.storage.insert_element(
			{
				'movieId': str(movie_id),
				'userId': str(user_id),
				'rank': str(rank)
			},
			settings.MONGO_LIKE_COLLECTION
		)
		return ScoreResponseSchema(
			movie_id=movie_id,
			user_id=user_id,
			rank=rank
		)

	async def delete_like(
		self, user_id: UUID, movie_id: UUID
	) -> DeleteScoreResponseSchema | None:
		if not await self._is_movie_exists(movie_id):
			return None

		await self.storage.delete_element(
			{
				'movieId': str(movie_id), 'userId': str(user_id)
			},
			settings.MONGO_LIKE_COLLECTION
		)
		return DeleteScoreResponseSchema(user_id=user_id, movie_id=movie_id)


@lru_cache()
def get_like_service(
	storage: Annotated[IStorage, Depends(get_storage)]
):
	return LikeService(storage)
