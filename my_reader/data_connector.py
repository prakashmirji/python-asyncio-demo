import asyncio
import json
import re
from collections import deque
import csv

import aiohttp

from my_reader.house_data import HouseData
from my_reader.logger import log

_data_regex = re.compile(r'data: (\[.*\])')
_headers = {'accept': 'application/json'}
async def receive_house_data(host, key, data_queue: deque, data_lock: asyncio.Lock):
    """ Receive data from S3 data source for house price and put it in a queue

    :param host: url of the data source to connect to
    :param key: token that will be used to authenticate against S3
    :param data_queue: queue that will contain the data from house data source
    :param data_lock: lock used to synchronize the queue's usage
    """

    log.info(f"Opening data from {host}")

    #url = f"https://{host}/id={key}"
    url = f"http://{host}"
    log.debug(f" url : {url}")

    async with aiohttp.ClientSession(headers=_headers) as session:
        async with session.get(url, timeout=None) as resp:
            if resp.status != 200:
                log.error(f"Connection to house data not successful: {resp.status} {resp.reason}")
                raise RuntimeError(f"Connection to house data not successful: {resp.status} {resp.reason}")

            async for line in resp.content:
                line = line.decode('utf8')
                log.debug(f"Received raw data")
                cr = csv.reader(line.splitlines(), delimiter=',')
                my_list = list(cr)
                for row in my_list[:5]: 
                    await data_lock.acquire()
                    try:
                        data_queue.append(row)
                    finally:
                        data_lock.release()
                    log.debug(f"row = {row}") 