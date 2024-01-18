from uuid import UUID
from pydantic import BaseModel, Field


class AddReviewToMovieSchema(BaseModel):
	movie_id: UUID
	text: str
	rank: int = Field(..., ge=0, le=10)


class ReviewResponseSchema(BaseModel):
	movie_id: UUID
	user_id: UUID
	text: str
	rank: int = Field(..., ge=0, le=10)
