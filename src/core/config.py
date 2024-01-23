import os

from pydantic_settings import BaseSettings
from logging import config as logging_config

from .logger import LOGGING


class Settings(BaseSettings):
    project_name: str = 'ugc'
    mongodb_url: str = 'mongodb://mongos1:27017'
    database_name: str = 'films_ugc'
    collection_name: str = 'events_ugc'
    sentry_dsn: str


logging_config.dictConfig(LOGGING)

settings = Settings()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
