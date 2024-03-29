import pytest
import pytest_asyncio
import uuid
from datetime import datetime
from http import HTTPStatus

from schemas.entity import FilmLikePayloads, FilmCommentPayloads, FilmCommentLikePayloads, FilmFavoritePayloads


@pytest.mark.parametrize(
    'event_data, expected_response, status_code',
    [
        (
            {
                    "collection_name": "events_ugc",
                    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "film_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
                    "created_at": "2024-01-24T12:09:56.434000",
                    "event_name": "film_likes",
                    "score": 0
                },
                {
                    "rec": {
                        "collection_name": "events_ugc",
                        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "film_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
                        "created_at": "2024-01-24T12:09:56.434000",
                        "event_name": "film_likes",
                        "score": 0
                    },
                    "msg": "Event was posted successfully",
                    "status_code": 200
                },
                HTTPStatus.OK,
        ),
    ]
)
async def test_post_event(
    make_post_request,
    create_fake_jwt,
    event_data,
    expected_response,
    status_code,
):
    fake_jwt = create_fake_jwt(event_data.get('user_id'))
    headers = {
        'X-Request-Id': str(uuid.uuid4()),
        'Authorization': f'Bearer {fake_jwt}'
    }
    result = await make_post_request('post_event/', event_data, headers)

    assert result.get('body').keys() == expected_response.keys()

    result.get('body').get('rec').pop('_id')

    assert result.get('body').get('rec') == expected_response.get('rec')
    assert result.get('status') == status_code


@pytest.mark.parametrize(
    'event_data, expected_response, status_code',
    [
        (
                {
                    "film_id": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
                },
                {
                    "avg_score": 0,
                    "film_id": "3fa85f64-5717-4562-b3fc-2c963f66afa8"
                },
                HTTPStatus.OK,
        ),
    ]
)
async def test_get_film_info(
        make_get_request,
        create_fake_film_like,
        event_data,
        expected_response,
        status_code,
):
    await create_fake_film_like()
    headers = {
        'X-Request-Id': str(uuid.uuid4()),
    }
    result = await make_get_request(f'film/{event_data.get("film_id")}', headers=headers)

    assert result.get('body') == expected_response
    assert result.get('status') == status_code


@pytest.mark.parametrize(
    'event_data, expected_response, status_code',
    [
        (
                {
                    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                },
                {
                    'body': [
                        {
                            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "film_id": "3fa85f64-5717-4562-b3fc-2c963f66afa4",
                            "created_at": "2024-01-24T12:09:56.434000",
                            "event_name": "film_favorites"
                        },
                        {
                            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "film_id": "3fa85f64-5717-4562-b3fc-2c963f66afa2",
                            "created_at": "2024-01-24T12:09:56.434000",
                            "event_name": "film_favorites"
                        }
                    ]
                },
                HTTPStatus.OK,
        ),
    ]
)
async def test_get_user_favorite_films_info(
    make_get_request,
    create_fake_jwt,
    create_fake_film_favorites,
    event_data,
    expected_response,
    status_code,
):
    await create_fake_film_favorites()
    fake_jwt = create_fake_jwt(event_data.get('user_id'))
    headers = {
        'X-Request-Id': str(uuid.uuid4()),
        'Authorization': f'Bearer {fake_jwt}'
    }
    result = await make_get_request(f'film_favorites', headers=headers)

    assert result.get('body') == expected_response.get('body')
    assert result.get('status') == status_code