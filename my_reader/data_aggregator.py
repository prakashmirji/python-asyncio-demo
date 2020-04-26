import asyncio
from collections import deque, defaultdict

from my_reader.logger import log
from my_reader.data_publisher import Publisher

async def publish_data(data_queue: deque, data_lock: asyncio.Lock, publisher: Publisher):
    """Publishes the data to the wamp topic

    :param data_queue: queue containing the several item of HouseData
    :param data_lock: lock used to synchronize the usage of the queue
    :param publisher: Publisher used to publish data on topic
    """

    log.info('Publishing data')

    data_per_house = []
    await data_lock.acquire()
    try:
        log.info(f"Received {len(data_queue)} data in the last hour")
        while data_queue:
            data = data_queue.pop()
            data_per_house.append(data)
    finally:
        data_lock.release()
    
    for h in data_per_house:
        # TODO do some transformation like data avg etc
        log.debug(f"publishing to topic : {h}")
        publisher.publish('conti.tutorial.hello', {'price': h})
    
    log.info(f"Published {len(data_per_house)} events")