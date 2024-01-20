import logging
from functools import lru_cache
from typing import Any
from uuid import UUID

from bson import ObjectId
from db.mongodb import MongoStorage
from db.storage import get_mongo
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from pymongo import ReturnDocument

from core.config import settings
from schemas.entity import UGCPayloads


def calculate_offset(page_size: int, page_number: int) -> int:
    return (page_number - 1) * page_size


class EventService:
    """Класс EventService содержит бизнес-логику по работе с событиями."""
    def __init__(
        self,
        mongo: MongoStorage
    ) -> None:
        self.mongo = mongo
        self.db = self.mongo.connection.get_database(settings.database_name)

    async def check_if_rec_exist(
        self,
        event_payloads: UGCPayloads,
    ) -> Any | None:
        """ Метод проверки существования записи в коллекции. """
        event_dto = jsonable_encoder(event_payloads)
        logging.info(event_dto)
        collection = self.db.get_collection(event_dto.get('collection_name'))
        return await collection.find_one(
            event_payloads.model_dump(
                exclude={'id', 'collection_name', 'created_at'}
            )
        )

    async def check_if_rec_exist_by_id(
        self,
        event_payloads: UGCPayloads,
    ) -> Any | None:
        """ Метод проверки существования записи в коллекции по _id. """
        event_dto = jsonable_encoder(event_payloads)
        collection = self.db.get_collection(event_dto.get('collection_name'))
        return await collection.find_one(
            {
                '_id': ObjectId(event_dto.get('_id')),
                'event_name': event_dto.get('event_name'),
            }
        )

    async def create_record(
        self,
        event_payloads: UGCPayloads,
    ):
        """ Метод создания записи в коллекцию. """
        event_dto = jsonable_encoder(event_payloads)
        collection = self.db.get_collection(event_dto.get('collection_name'))

        try:
            new_rec = await collection.insert_one(
                event_payloads.model_dump(
                    by_alias=True, exclude={'id', 'collection_name'}
                )
            )
            created_rec = await collection.find_one(
                {'_id': new_rec.inserted_id}
            )
            return created_rec
        except Exception as e:
            logging.error(e)

    async def update_record(
        self,
        event_payloads: UGCPayloads,
    ):
        """ Метод обновления записи в соответствующей коллекции. """
        event_dto = jsonable_encoder(event_payloads)
        collection = self.db.get_collection(event_dto.get('collection_name'))

        update_rec = await collection.find_one_and_update(
            {
                '_id': ObjectId(event_dto.get('_id'))
            },
            {
                '$set': event_payloads.model_dump(
                    by_alias=True, exclude={'id', 'collection_name'}
                )
            },
            return_document=ReturnDocument.AFTER
        )

        return update_rec

    async def get_film_info(
        self,
        film_id: UUID,
    ) -> list:
        """ Метод получения информации о фильме. """
        collection = self.db.get_collection(settings.collection_name)
        pipeline_film = [
            {
                '$match': {
                    'film_id': str(film_id)
                }
            },
            {
                '$group': {
                    '_id': {
                        'film_id': '$film_id'
                    },
                    'avg_score': {'$avg': '$score'}
                }
            },
            {
                '$project':
                    {
                        '_id': 0,
                        'film_id': '$_id.film_id',
                        'avg_score': 1
                    }
            },
        ]
        return [rec async for rec in collection.aggregate(pipeline_film)]

    async def get_film_favorites(
        self,
        user_id: UUID,
    ) -> list:
        """ Метод получения списка избранных фильмов пользователя. """
        collection = self.db.get_collection(settings.collection_name)
        recs = collection.find(
            {
                'user_id': str(user_id),
                'event_name': 'film_favorites'
            },
            {'_id': 0}
        )
        return [rec async for rec in recs]

    async def get_film_comments(
        self,
        film_id: UUID,
        page_size: int,
        page_number: int,
    ) -> list:
        """ Метод получения списка комментариев к фильму. """
        collection = self.db.get_collection(settings.collection_name)
        pipeline_comments = [
            {
                '$match': {
                    'film_id': str(film_id),
                    'event_name': 'film_comments'
                }
            },
            {
                '$sort': {
                    'created_at': -1
                }
            },
            {
                '$project': {
                    '_id': 0
                }
            },
            {
                '$skip': calculate_offset(page_size, page_number)
            },
            {
                '$limit': page_size
            }
        ]
        return [rec async for rec in collection.aggregate(pipeline_comments)]


@lru_cache()
def get_event_service(
    mongo: MongoStorage = Depends(get_mongo),
) -> EventService:
    return EventService(mongo)
