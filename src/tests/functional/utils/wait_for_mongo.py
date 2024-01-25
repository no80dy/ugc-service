import logging
import time
import backoff

from requests.exceptions import Timeout, ConnectionError
from motor.motor_asyncio import AsyncIOMotorClient


mongodb_url = 'mongodb://mongo:27017'

BACKOFF_MAX_TIME = 60

if __name__ == '__main__':
    mongo_client = AsyncIOMotorClient(
        host=mongodb_url,
    )


    @backoff.on_exception(
        backoff.expo,
        (Timeout, ConnectionError,),
        max_time=BACKOFF_MAX_TIME
    )
    def check_mongo_readiness():
        while True:
            if mongo_client.admin.command('ping'):
                logging.info('Mongo ping Ok')
                break
            time.sleep(1)


    try:
        check_mongo_readiness()
    except ConnectionError:
        logging.info('Mongo is not available')
        raise ConnectionError
