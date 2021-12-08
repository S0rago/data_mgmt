from asyncio.tasks import sleep
import logging
import os
import json

from redis import client

from kafka import KafkaConsumer
from asyncio import get_event_loop, ensure_future
from aiohttp.web import Application, AppRunner, TCPSite
from aiohttp import ClientSession
import logging
from redis.client import Redis
import sys

if __name__ == "__main__":

    service_name = os.getenv("service_name")

    logger = logging.getLogger(service_name)
    logger.setLevel(logging.INFO)
    logger.info("Consumer started")
    print("Consumer started")

    topic = os.getenv("topic")
    encoding = os.getenv("ENCODING")

    consumer = KafkaConsumer(
        topic,
        api_version=(0, 10, 2),
        value_deserializer=lambda v: json.loads(v.decode(encoding)),
        bootstrap_servers=[os.getenv("server")]
    )

    redis = Redis(
        host=os.getenv("REDIS_HOST"),
        port=os.getenv("REDIS_PORT"),
        decode_responses=True
    )

    redis_key = "logs"

    async def looped(loop=None):
        async with ClientSession() as client_session:
            while True:
                try:
                    for msg in consumer:
                        msg = msg.value
                        logger.info(msg)
                        print("msg:", msg)
                        
                        value = redis.get(redis_key)
                        print("value:", value)
                        if not value:
                            value = [msg]
                        else: 
                            value = json.loads(value)
                            value.append(msg)

                        print(redis.set(redis_key, json.dumps(value)))
                        print(redis.get(redis_key))
                        sys.stdout.flush()
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