from json import dumps
import os 

from aiohttp.web import Request, Response
from kafka import KafkaProducer

class Controller:
    
    def __init__(self, service_name, topic, producer: KafkaProducer):
        self.service_name = service_name
        self.topic = topic
        self.producer = producer
        self.encoding = os.getenv('ENCODING')


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

        return Response(body=dumps(result), status=status, content_type="application/json")
        
    