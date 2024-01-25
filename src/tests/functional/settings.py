from pydantic_settings import BaseSettings


class TestSettings(BaseSettings):
	mongodb_url: str = 'mongodb://mongo:27017'
	database_name: str = 'films_ugc'
	collection_name: str = 'events_ugc'

	JWT_SECRET_KEY: str = 'secret'
	JWT_ALGORITHM: str = 'HS256'

	SERVICE_URL: str = 'http://ugc_service:8000'


test_settings = TestSettings()
