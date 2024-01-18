from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends, Body, HTTPException

from schemas.likes import (
	ScoreResponseSchema,
	AddScoreToMovieSchema,
	DeleteScoreFromMovieSchema,
	DeleteScoreResponseSchema
)
from services.likes import LikeService, get_like_service
from .auth import security_jwt


router = APIRouter()


@router.post(
	'/',
	response_model=ScoreResponseSchema,
	summary='Добавление лайка к фильму',
	description='По идентификатору пользователя и фильма производится добавление лайка',
	response_description='Информация о добавленном лайке'
)
async def add_like_to_movie(
	user: Annotated[dict, Depends(security_jwt)],
	like_body: Annotated[AddScoreToMovieSchema, Body()],
	like_service: LikeService = Depends(get_like_service)
) -> ScoreResponseSchema:
	like = await like_service.add_like(
		user.get('user_id'), like_body.movie_id, like_body.rank
	)
	if not like:
		raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Not found')
	return like


@router.delete(
	'/',
	response_model=DeleteScoreResponseSchema,
	summary='Удаление лайка из фильма',
	description='По идентификатору пользователя и фильма производится удаление лайка',
	response_description='Информация об удаленном лайке'
)
async def delete_like_from_movie(
	user: Annotated[dict, Depends(security_jwt)],
	like_body: Annotated[DeleteScoreFromMovieSchema, Body()],
	like_service: LikeService = Depends(get_like_service)
) -> DeleteScoreResponseSchema:
	like = await like_service.delete_like(
		user.get('user_id'), like_body.movie_id
	)
	if not like:
		raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Not found')
	return like
