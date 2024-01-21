import os

from pydantic_settings import BaseSettings
from logging import config as logging_config

from .logger import LOGGING


class Settings(BaseSettings):
    project_name: str = 'ugc'
    mongodb_url: str = 'mongodb://mongos1:27017'
    database_name: str = 'films_ugc'
    collection_name: str = 'events_ugc'
    sentry_dsn: str = 'https://6af7af3b93767de623be7b1ede9f65dd@o4506569432039424.ingest.sentry.io/4506603489460224'


logging_config.dictConfig(LOGGING)

settings = Settings()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
