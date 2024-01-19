from datetime import datetime
from http import HTTPStatus
from typing import Union
from uuid import UUID

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated, Literal, Optional


# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


class UGCPayloads(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    collection_name: str = 'events_ugc'
    user_id: UUID
    film_id: UUID
    created_at: Optional[datetime] = datetime.utcnow()

    @field_validator("user_id", "film_id")
    def validate_uuids(cls, value: UUID) -> str:
        return str(value)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )


class FilmLikePayloads(UGCPayloads):
    event_name: Literal['film_likes']
    score: int = Field(ge=0, le=10)


class FilmCommentPayloads(UGCPayloads):
    event_name: Literal['film_comments']
    film_comment: str = Field(max_length=256)


class FilmCommentLikePayloads(UGCPayloads):
    event_name: Literal['comment_likes']
    comment_id: PyObjectId


class FilmFavoritePayloads(UGCPayloads):
    event_name: Literal['film_favorites']


class ResponseModel(BaseModel):
    """Модель ответа при успешном добавлении события в базу данных."""
    rec: Union[FilmLikePayloads, FilmCommentPayloads, FilmCommentLikePayloads, FilmFavoritePayloads]
    msg: str = 'Event was posted successfully'
    status_code: int = HTTPStatus.OK
