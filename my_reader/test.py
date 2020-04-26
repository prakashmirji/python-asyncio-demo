import argparse
import asyncio
import datetime
from collections import deque
import sys

from data_publisher import create_publisher, Publisher
from data_aggregator import publish_data
from data_connector import receive_house_data
from logger import log

async def run_tasks(host, key):
    log.info(f"Entered run_tasks")
    data_queue = deque()
    data_lock = asyncio.Lock()
    connector_task = asyncio.create_task(receive_house_data(host, key, data_queue, data_lock))

    await asyncio.gather(
        connector_task
    )

    while data_queue:
        log.debug(f" data = {data_queue.pop()}")
        log.debug(f"price row = {data_queue.pop().}")

if __name__ == "__main__":
    host = 'samplecsvs.s3.amazonaws.com/Sacramentorealestatetransactions.csv'
    key = 100
    log.setLevel('DEBUG')
    asyncio.run(run_tasks(host, key))