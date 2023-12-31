import backoff

from kafka.errors import KafkaError
from clickhouse_driver.errors import Error as ClickHouseError

from models import UserActivityModel
from settings import settings
from queries import insert_query
from logger import logger
from managers import KafkaConsumerManager, ClickHouseClientManager


BACKOFF_MAX_TIME = 60


def consume_messages(consumer):
    user_activity_batch = []
    for message in consumer:
        user_activity = UserActivityModel(**message.value)
        user_activity_batch.append(user_activity)
        logger.info(f'Added in batch {user_activity}')

        if len(user_activity_batch) >= settings.batch_size:
            return user_activity_batch


def process_user_activity_batch(user_activity_batch, client):
    client.execute(
        insert_query,
        [
            {
                'id': str(user_activity_item.id),
                'user_id': str(user_activity_item.user_id),
                'film_id': str(user_activity_item.film_id),
                'event_name': user_activity_item.event_name,
                'comment': user_activity_item.comment,
                'film_sec': user_activity_item.film_sec,
                'like': user_activity_item.like,
                'event_time': user_activity_item.event_time.replace(microsecond=0),
            }
            for user_activity_item in user_activity_batch
        ]
    )
    logger.info(f'Loaded to ClickHouse {len(user_activity_batch)}')


@backoff.on_exception(
    backoff.expo,
    (KafkaError, ClickHouseError, ),
    max_time=BACKOFF_MAX_TIME,
    logger=logger
)
def load_data_to_clickhouse():
    with KafkaConsumerManager() as consumer, ClickHouseClientManager() as client:
        try:
            while True:
                user_activity_batch = consume_messages(consumer)
                if user_activity_batch:
                    process_user_activity_batch(user_activity_batch, client)
                    consumer.commit()
        except KeyboardInterrupt:
            logger.info("Stopping ETL pipeline...")


if __name__ == '__main__':
    try:
        load_data_to_clickhouse()
    except Exception as e:
        logger.error(f'Unexpected error: {e}')
