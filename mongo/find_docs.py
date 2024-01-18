import asyncio
from motor.motor_asyncio import AsyncIOMotorClient


async def show_movies():
	client = AsyncIOMotorClient(
		'mongodb://localhost:27019,localhost:27020'
	)
	db = client['moviesDb']
	collection = db['movies']
	
	cursor = collection.find()
	
	async for document in cursor:
		print(document)
	
	client.close()


if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(show_movies())
