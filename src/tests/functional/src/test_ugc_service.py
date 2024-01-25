import pytest
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
                    "created_at": "2024-01-24T12:09:56.434178",
                    "event_name": "film_likes",
                    "score": 0
                },
                {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "first_name": "string",
                    "last_name": "string",
                    "groups": []
                },
                HTTPStatus.OK,
        ),
    ]
)
async def test_post_event(
        make_post_request,
        event_data,
        expected_response,
        status_code,
):
    headers = {
        'X-Request-Id': uuid.uuid4()
    }
    result = await make_post_request('post_event', event_data, headers)

    # assert result.get('body').keys() == expected_response.keys()
    #
    # result.get('body').pop('id')
    # expected_response.pop('id')
    #
    # assert result.get('body') == expected_response
    assert result.get('status') == status_code
