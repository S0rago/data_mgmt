import os
import json

from kafka import KafkaProducer
from controller import Controller
from asyncio import get_event_loop, ensure_future
from aiohttp.web import Application, AppRunner, TCPSite
from logging import getLogger

if __name__ == "__main__":

    logger = getLogger("GetApp")
    logger.debug("started")
    
    service_name = os.getenv("service_name")
    topic = os.getenv("topic")

    producer = KafkaProducer(
        api_version=(0, 10, 2),
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        bootstrap_servers=[os.getenv("server")]
    )
    
    controller = Controller(service_name, topic, producer)

    async def main(loop=None):
        application = Application(logger=logger)
        application.router.add_post("/api/v1/sendmsg", controller.add_data)

        runner = AppRunner(application)

        await runner.setup()

        site = TCPSite(runner, os.getenv("host"), os.getenv("port"))
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