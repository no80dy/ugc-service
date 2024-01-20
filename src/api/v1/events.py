from http import HTTPStatus
from typing import Annotated, Union
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse

from schemas.entity import (
    FilmCommentLikePayloads,
    FilmCommentPayloads,
    FilmFavoritePayloads,
    FilmLikePayloads,
    ResponseModel,
)
from services.event import EventService, get_event_service


router = APIRouter()


@router.post(
    '/post_event',
    summary='Сбор статистики',
    description=(
    'Принимает события, связанные с фильмами,'
    'от конкретного пользователя: лайки, комментарии,'
    'лайки комментариев, любимые фильмы'
    ),
    response_description="Add new event",
    response_model=ResponseModel,
)
async def post_event(
    event_payloads: Union[
        FilmLikePayloads,
        FilmCommentPayloads,
        FilmCommentLikePayloads,
        FilmFavoritePayloads,
    ],
    event_service: EventService = Depends(get_event_service),
):
    if await event_service.check_if_rec_exist(event_payloads):
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content={
                'detail': 'event have already exist in database'
            }
        )
    else:
        rec = await event_service.create_record(event_payloads)
        return {'rec': rec}


@router.put(
    '/put_event',
    summary='Обновление статистики',
    description=(
        'Принимает события, связанные с фильмами,'
        'от конкретного пользователя: лайки, комментарии,'
        'лайки комментариев, любимые фильмы'
    ),
    response_description="Update existing event",
    response_model=ResponseModel,
)
async def post_event(
    event_payloads: Union[
        FilmLikePayloads,
        FilmCommentPayloads,
        FilmCommentLikePayloads,
        FilmFavoritePayloads,
    ],
    event_service: EventService = Depends(get_event_service),
):
    if not await event_service.check_if_rec_exist_by_id(event_payloads):
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content={
                'detail': 'event does not exist in database',
            }
        )
    else:
        rec = await event_service.update_record(event_payloads)
        return {'rec': rec}


@router.get(
    '/film/{film_id}',
    summary='Информация о фильме',
    description=(
    'Отдает информацию по фильму: лайки, комментарии,'
    'лайки комментариев, любимые фильмы'
    ),
    response_description="Get film information",
)
async def get_film_info(
    film_id: UUID,
    event_service: EventService = Depends(get_event_service),
):
    res = await event_service.get_film_info(film_id)
    if len(res) > 0:
        return res[0]
    else:
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content={
                'detail': 'film_id does not found in database',
            }
        )


@router.get(
    '/film_favorites/{user_id}',
    summary='Информация об избранных фильмах пользователя',
    response_description="Get user favorite films information",
)
async def get_film_info(
    user_id: UUID,
    event_service: EventService = Depends(get_event_service)
) -> list:
    return await event_service.get_film_favorites(user_id)


@router.get(
    '/film_comments/{film_id}',
    summary='Список комментариев к фильму',
    response_description="Film comments list",

)
async def get_film_comments(
    film_id: UUID,
    page_size: Annotated[int, Query(description='Размер страницы', ge=1)] = 20,
    page_number: Annotated[int, Query(description='Номер страницы', ge=1)] = 1,
    event_service: EventService = Depends(get_event_service)
) -> list:
    return await event_service.get_film_comments(
        film_id, page_size, page_number
    )
