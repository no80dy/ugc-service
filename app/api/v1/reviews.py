from uuid import UUID
from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends, Body, HTTPException, Query

from services.reviews import ReviewService, get_review_service
from schemas.reviews import AddReviewToMovieSchema, ReviewResponseSchema
from .auth import security_jwt


router = APIRouter()

NOT_FOUND_DETAILS = 'Films with such identifier not found'


@router.get(
	'/',
	response_model=list[ReviewResponseSchema],
	summary='Добавление рецензии к фильму',
	description='По идентификатору пользователя и фильма добавляет рецензию',
	response_description='Информация о добавленной рецензии к фильму'
)
async def add_review_in_movie(
	movie_id: Annotated[UUID, Query()],
	review_service: ReviewService = Depends(get_review_service)
) -> list[ReviewResponseSchema]:
	reviews = await review_service.get_reviews_for_movie(movie_id)
	if not reviews:
		raise HTTPException(
			status_code=HTTPStatus.NOT_FOUND, detail=NOT_FOUND_DETAILS
		)
	return reviews


@router.post(
	'/',
	response_model=ReviewResponseSchema,
	summary='Добавление рецензии к фильму',
	description='По идентификатору пользователя и фильма добавляет рецензию',
	response_description='Информация о добавленной рецензии к фильму'
)
async def add_review_in_movie(
	user: Annotated[dict, Depends(security_jwt)],
	review_body: Annotated[AddReviewToMovieSchema, Body()],
	review_service: ReviewService = Depends(get_review_service)
) -> ReviewResponseSchema:
	review = await review_service.add_review_in_movie(
		user.get('user_id'), review_body.movie_id, review_body.text, review_body.rank
	)
	if not review:
		raise HTTPException(
			status_code=HTTPStatus.NOT_FOUND, detail=NOT_FOUND_DETAILS
		)
	return review
