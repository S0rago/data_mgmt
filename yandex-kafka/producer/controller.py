import os 

from aiohttp.web import Request, Response
from aiohttp_rest_api import AioHTTPRestEndpoint
from aiohttp_rest_api.responses import respond_with_json
from asyncio import get_event_loop, wait, shield
from json import loads, dumps
from uuid import uuid4
from kafka import KafkaProducer
from redis.client import Redis

class Controller:
    
    def __init__(self, service_name, topic, producer: KafkaProducer):
        self.service_name = service_name
        self.topic = topic
        self.producer = producer
        self.encoding = os.getenv('ENCODING')
        self.redis = Redis(
            host=os.getenv("REDIS_HOST"),
            port=os.getenv("REDIS_PORT"),
            decode_responses=True
        )

    async def add_data(self, request: Request) -> Response:
        if request.has_body:
            json = await request.json()
        
        future = self.producer.send(self.topic, json)
        
        if future is not None:
            result = future.get(timeout=60)
            status=200
        else:
            result = {"message": "Message send timeout"}
            status=500

        response = respond_with_json(result, status)
        return response

    async def get_data(self, request: Request) -> Response:
        if request.query:
            key = request.query['key']
            
        value = self.redis.get(key)
        
        if value is not None:
            result = loads(value)
            status=200
        else:
            result = {"message": "Not found"}
            status=404

        response = respond_with_json(result, status)
        return response

    