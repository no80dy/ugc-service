from abc import ABC, abstractmethod

import motor.motor_asyncio


class IStorage(ABC):
    @abstractmethod
    async def close(self):
        pass


class MongoStorage(IStorage):
    def __init__(self, **kwargs) -> None:
        self.connection = motor.motor_asyncio.AsyncIOMotorClient(**kwargs)

    async def close(self):
        await self.connection.close()
