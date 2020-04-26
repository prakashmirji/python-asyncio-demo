import argparse
import asyncio
import datetime
from collections import deque

from my_reader.data_publisher import create_publisher, Publisher
from my_reader.data_aggregator import publish_data
from my_reader.data_connector import receive_house_data
from my_reader.logger import log

def seconds_until_next_hour():
    """Counts the number of seconds until the next "round" hour.
    e.g. if it is 14:25:35, there are 2065s until 15:00:00

    :return number of seconds until next hour
    """

    now = datetime.datetime.now()
    now_minute = now.minute
    now_second = now.second

    seconds_left = (60 - now_minute) * 60 - now_second
    log.debug(f"{seconds_left} seconds left until next round hour")
    return seconds_left

async def publish_hourly(data_queue: deque, data_lock: asyncio.Lock, publisher: Publisher):
    """Method that will publish data each hour
    :param data_queue: queue that will contain house data
    :param data_lock: lock used to synchronize the queue
    :param publisher: Publisher used to publish data to crossbar topic
    """
    log.info('Starting hourly publication')

    # sleep until first round hour
    #await asyncio.sleep(seconds_until_next_hour())
    # TODO - testing
    await asyncio.sleep(1)
    while True:
        await publish_data(data_queue, data_lock, publisher)
        #await asyncio.sleep(seconds_until_next_hour())
        # TODO - testing
        await asyncio.sleep(1)

async def run_tasks(host, key, crossbar_host):
    """Orchestrator that will plan and launch all the tasks"""
    log.info('Starting demo-fom application')

    # publisher used to publish on crossbar
    publisher = await create_publisher(crossbar_host)
    log.info('Publisher created')

    # data structures used to share information across tasks
    data_queue = deque()
    data_lock = asyncio.Lock()

    connector_task = asyncio.create_task(receive_house_data(host, key, data_queue, data_lock))
    publish_task = asyncio.create_task(publish_hourly(data_queue, data_lock, publisher))

    await asyncio.gather(
        connector_task, publish_task
    )

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='host url of house data source', required=True)
    parser.add_argument('-k', '--key', help='key used to connect to data stream', required=True)
    parser.add_argument('-c', '--crossbar', help='host url of crossbar', required=True)
    parser.add_argument('-v', '--verbosity', help='level of verbosity of the application',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='INFO')

    args = parser.parse_args()
    return args.url, args.key, args.crossbar, args.verbosity

def exec_app():
    """Entry point of the whole application"""
    host, key, crossbar_host, verbosity = parse_args()

    log.setLevel(verbosity)

    asyncio.run(run_tasks(host, key, crossbar_host))