from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	PROJECT_NAME: str = 'ugc-service'

	MONGODB_HOSTS: str

	MONGO_DATABASE_NAME: str = 'moviesDb'
	MONGO_REVIEW_COLLECTION: str = 'reviews'
	MONGO_LIKE_COLLECTION: str = 'likes'
	MONGO_BOOKMARK_COLLECTION: str = 'bookmarks'
	MONGO_MOVIE_COLLECTION: str = 'movies'

	JWT_SECRET_KEY: str = 'secret'
	JWT_ALGORITHM: str = 'HS256'


settings = Settings()
