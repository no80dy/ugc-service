import logging
import sys
import time
import backoff
import requests

from motor.motor_asyncio import AsyncIOMotorClient
from pathlib import Path
# from functional.settings import test_settings

# sys.path.append(str(Path(__file__).resolve().parents[3]))

mongodb_url = 'mongodb://mongos1:27017'

BACKOFF_MAX_TIME = 60

if __name__ == '__main__':
    mongo_client = AsyncIOMotorClient(
        # host=test_settings.mongodb_url,
        host=mongodb_url,
    )


    @backoff.on_exception(
        backoff.expo,
        (requests.exceptions.Timeout, requests.exceptions.ConnectionError,),
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
        print('Mongo is not available')
        raise ConnectionError
