import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = 'ugc'
    mongodb_url: str = 'mongodb://mongos1:27017'
    database_name: str = 'films_ugc'
    collection_name: str = 'events_ugc'


settings = Settings()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
