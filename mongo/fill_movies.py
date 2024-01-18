import asyncio
import random
import uuid
from uuid import uuid4, UUID
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient


async def create_movies():
	client = AsyncIOMotorClient(
		'mongodb://localhost:27019,localhost:27020'
	)
	db = client['moviesDb']
	collection = db['movies']

	movies = []
	for _ in range(100):
		movie = {
			"_id": str(uuid.uuid4())
		}
		movies.append(movie)

	result = await collection.insert_many(movies)
	print(f'{len(result.inserted_ids)} movies inserted.')

	client.close()


if __name__ == '__main__':
	random.seed(20)
	asyncio.run(create_movies())
