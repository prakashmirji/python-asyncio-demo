import asyncio
import os

import txaio
from autobahn.asyncio.component import Component
from my_reader.logger import log

async def create_publisher(crossbar_url):
    """ Create a publisher with a valid session

    :param crossbar_url: url against which the session is supposed to be established
    :return: a published once the session has been established
    """

    publisher = Publisher()
    await publisher.connect(crossbar_url)

    return publisher

class Publisher:
    def __init__(self):
        self.component = None

    async def connect(self, crossbar_url):
        """Method used to initialize a session for the publisher

        :param crossbar_url: url hosting the crossbar instance
        """
        log.debug(f"Connecting to {crossbar_url}")

        self.component = Component(
            transports=crossbar_url,
            realm='realm1'
        )

        loop = asyncio.get_event_loop()
        txaio.config.loop = loop

        session_ready = asyncio.Event()

        async def setup_session(created_session, _details):
            """Callback method used to retrieve a session and notify interested parties with an event"""
            self.session = created_session
            nonlocal session_ready
            session_ready.set()
        
        self.component.start(loop=loop)
        self.component.on_join(setup_session)

        await session_ready.wait()

    def publish(self, topic, payload):
        """Publish the payload on the specified topic

        :param topic: target topic
        :param payload: payload to be published
        """
        self.session.publish(topic, payload)
        log.debug(f"data is published to : {topic}")