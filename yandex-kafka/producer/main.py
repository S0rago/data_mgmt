import os
import json

from kafka import KafkaProducer
from controller import Controller
from asyncio import get_event_loop, ensure_future
from aiohttp.web import Application, AppRunner, TCPSite
import logging

if __name__ == "__main__":

    service_name = os.getenv("SERVICE_NAME")
    
    logger = logging.getLogger(service_name)
    logger.debug("Producer started")
    
    
    topic = os.getenv("TOPIC")

    producer = KafkaProducer(
        api_version=(0, 10, 2),
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        bootstrap_servers=[os.getenv("SERVER")]
    )
    
    controller = Controller(service_name, topic, producer)

    async def main(loop=None):
        application = Application(logger=logger)
        application.router.add_post("/afonin/api/v1/sendmsg", controller.add_data)

        runner = AppRunner(application)

        await runner.setup()

        site = TCPSite(runner, os.getenv("HOST"), os.getenv("PORT"))
        await site.start()
    
    loop = get_event_loop()
    try:
        ensure_future(main(loop), loop=loop)
        loop.run_forever()
    except RuntimeError as exc:
        logger.exception(exc)
        raise(exc)
    finally:
        loop.run_until_complete(main(loop))
        loop.close()