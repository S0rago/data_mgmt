from asyncio.tasks import sleep
import logging
import os
import json
import sys

from aiohttp.client_reqrep import ClientResponse


from kafka import KafkaConsumer
from asyncio import get_event_loop, ensure_future
from aiohttp import ClientSession
import logging
from urllib.parse import quote_plus as quote

if __name__ == "__main__":

    service_name = os.getenv("SERVICE_NAME")

    logger = logging.getLogger(service_name)
    logger.debug("Consumer started")

    topic = os.getenv("TOPIC")
    encoding = os.getenv("ENCODING")
    
    mongo_host = os.getenv("MONGO_HOST")
    mogno_port = os.getenv("MONGO_PORT")
    mongo_api = os.getenv("MONGO_API")
    mongo_base_path = f'http://{mongo_host}:{mogno_port}/{mongo_api}'
    
    consumer = KafkaConsumer(
        topic,
        api_version=(0, 10, 2),
        value_deserializer=lambda v: json.loads(v.decode(encoding)),
        bootstrap_servers=[os.getenv("SERVER")]
    )

    
    async def save_to_db(msg, client_session):
        cresponse: ClientResponse = await client_session.post(url=mongo_base_path + '/add',
                                                                data=json.dumps(msg.value))
        return cresponse


    async def looped(loop=None):
        async with ClientSession() as client_session:
            while True:
                try:
                    for msg in consumer:
                        await save_to_db(msg, client_session)
                except Exception as exc:
                    logger.exception(exc)
                await sleep(5, loop=loop)


    loop = get_event_loop()
    try:
        ensure_future(looped(loop), loop=loop)
        loop.run_forever()
    except RuntimeError as exc:
        logger.exception(exc)
        raise(exc)
    finally:
        loop.run_until_complete(looped(loop))
        loop.close()
