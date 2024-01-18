from uuid import UUID
from pydantic import BaseModel, Field


class AddScoreToMovieSchema(BaseModel):
	movie_id: UUID
	rank: int = Field(..., ge=0, le=10)


class DeleteScoreFromMovieSchema(BaseModel):
	movie_id: UUID


class DeleteScoreResponseSchema(BaseModel):
	user_id: UUID
	movie_id: UUID


class ScoreResponseSchema(BaseModel):
	movie_id: UUID
	user_id: UUID
	rank: int = Field(..., ge=0, le=10)