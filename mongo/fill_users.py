import asyncio
import random
from uuid import uuid4, UUID
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient


users = [
	{'_id': '86830a5a-4b8c-4ea3-91f6-a2b6e03bdc50', 'username': 'Michail'},
	{'_id': 'f46e2fed-1cc6-4797-9c96-f2558a9203ff', 'username': 'Aleksandr'},
	{'_id': 'f5930779-b863-41ff-8f8f-bf92f73274d3', 'username': 'Sergey'},
	{'_id': '12f5fc5b-3ca3-46cf-bdd1-02b0e1ca32f4', 'username': 'Aleksey'},
	{'_id': '4b034370-f3c9-4dac-9cb8-95030768cfad', 'username': 'Vladimir'},
]


async def create_movies():
	client = AsyncIOMotorClient(
		'mongodb://localhost:27019,localhost:27020'
	)
	db = client['moviesDb']
	collection = db['users']

	result = await collection.insert_many(users)
	print(f'{len(result.inserted_ids)} users inserted.')
	client.close()


if __name__ == '__main__':
	random.seed(20)
	asyncio.run(create_movies())
