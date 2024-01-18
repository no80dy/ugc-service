from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends, Body, HTTPException

from schemas.bookmarks import (
	BookmarkResponseSchema,
	AddMovieInBookmarkSchema,
	DeleteMovieFromBookmarkSchema
)
from services.bookmarks import BookmarkService, get_bookmark_service
from .auth import security_jwt


router = APIRouter()


NOT_FOUND_DETAILS = 'Films with such identifier not found'

@router.get(
	'/',
	response_model=list[BookmarkResponseSchema],
	summary='Получение фильмов, добавленных в закладки',
	description='По идентификатору пользователя высвечивает список всех фильмов, добавленных в закладки',
	response_description='Список фильмов в закладках'
)
async def get_bookmarks(
	user_data: Annotated[dict, Depends(security_jwt)],
	bookmark_service: BookmarkService = Depends(get_bookmark_service)
) -> list[BookmarkResponseSchema]:
	bookmarks = await bookmark_service.get_user_bookmarks(user_data.get('user_id'))
	if not bookmarks:
		return []
	return bookmarks


@router.post(
	'/',
	response_model=BookmarkResponseSchema,
	summary='Добавление фильма в закладки',
	description='Добавление определенному пользователю фильма в закладки',
	response_description='Информация о добавленном фильме в закладках'
)
async def add_bookmarks(
	user: Annotated[dict, Depends(security_jwt)],
	movie_body: Annotated[AddMovieInBookmarkSchema, Body()],
	bookmark_service: BookmarkService = Depends(get_bookmark_service)
) -> BookmarkResponseSchema | None:
	bookmark = await bookmark_service.add_movie_in_bookmark(
		user.get('user_id'), movie_body.movie_id
	)
	if not bookmark:
		raise HTTPException(
			status_code=HTTPStatus.NOT_FOUND, detail=NOT_FOUND_DETAILS
		)
	return bookmark


@router.delete(
	'/',
	response_model=BookmarkResponseSchema,
	summary='Удаление фильма из закладок',
	description='Удаление у определенного пользователя фильма из закладок',
	response_description='Информация об удаленном фильме из закладках'
)
async def delete_bookmarks(
	user: Annotated[dict, Depends(security_jwt)],
	movie_body: Annotated[DeleteMovieFromBookmarkSchema, Body()],
	bookmark_service: BookmarkService = Depends(get_bookmark_service)
) -> BookmarkResponseSchema | None:
	bookmark = await bookmark_service.delete_user_bookmark(
		user.get('user_id'), movie_body.movie_id
	)
	if not bookmark:
		raise HTTPException(
			status_code=HTTPStatus.NOT_FOUND, detail=NOT_FOUND_DETAILS
		)
	return bookmark
