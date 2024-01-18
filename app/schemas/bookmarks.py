from uuid import UUID
from pydantic import BaseModel


class AddMovieInBookmarkSchema(BaseModel):
	movie_id: UUID


class DeleteMovieFromBookmarkSchema(BaseModel):
	movie_id: UUID


class BookmarkResponseSchema(BaseModel):
	movie_id: UUID
	user_id: UUID
