from uuid import UUID
from typing import Annotated
from functools import lru_cache
from fastapi import Depends

from db.storages import IStorage, get_storage
from schemas.reviews import ReviewResponseSchema
from core.config import settings


class ReviewService:
	def __init__(
		self, storage: IStorage
	) -> None:
		self.storage = storage

	async def _is_movie_exists(
		self, movie_id: UUID
	) -> bool:
		return await self.storage.find_element_by_properties(
			{'_id': str(movie_id)}, settings.MONGO_MOVIE_COLLECTION
		)

	async def add_review_in_movie(
		self,
		user_id: UUID,
		movie_id: UUID,
		text: str,
		rank: int
	) -> ReviewResponseSchema | None:
		if not await self._is_movie_exists(movie_id):
			return None

		await self.storage.insert_element(
			{
				'userId': str(user_id),
				'movieId': str(movie_id),
				'text': text,
				'rank': rank
			},
			settings.MONGO_REVIEW_COLLECTION
		)
		return ReviewResponseSchema(
			user_id=user_id,
			movie_id=movie_id,
			text=text,
			rank=rank
		)

	async def get_reviews_for_movie(
		self, movie_id: UUID
	) -> list[ReviewResponseSchema]:
		if not await self._is_movie_exists(movie_id):
			return []

		reviews = await self.storage.find_elements_by_properties(
			{'movieId': str(movie_id)}, settings.MONGO_REVIEW_COLLECTION
		)

		return [
			ReviewResponseSchema(
				user_id=review['userId'],
				movie_id=review['movieId'],
				text=review['text'],
				rank=review['rank']
			)
			for review in reviews
		]


@lru_cache
def get_review_service(
	storage: Annotated[IStorage, Depends(get_storage)]
) -> ReviewService:
	return ReviewService(storage)
