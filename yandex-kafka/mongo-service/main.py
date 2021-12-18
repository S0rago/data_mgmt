import os

from controller import ControllerMongo
from asyncio import get_event_loop, ensure_future
from aiohttp.web import Application, AppRunner, TCPSite
import logging

if __name__ == "__main__":

    service_name = os.getenv("SERVICE_NAME")
    
    logger = logging.getLogger(service_name)
    logger.debug("DB-service started")

    current_db = os.getenv("CURRENT_DB")
    controller = ControllerMongo(service_name)
    

    async def main(loop=None):
        application = Application(logger=logger)
        application.router.add_post("/afonin/api/v1/mongo/add", controller.add_data)
        application.router.add_get("/afonin/api/v1/mongo/get", controller.get_data)

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
