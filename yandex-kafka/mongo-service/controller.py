import os

from aiohttp.web import Request, Response
from json import dumps, loads
from pymongo import MongoClient
from datetime import datetime


class ControllerMongo:
    def __init__(self, service_name):
        self.service_name = service_name
        self.encoding = os.getenv('ENCODING')
        self.mongo_client = MongoClient(host=os.getenv("MONGO_HOST"),
                                        port=int(os.getenv("MONGO_PORT")),
                                        username=os.getenv("MONGO_USER"),
                                        password=os.getenv("MONGO_PASS"))
        self.db = self.mongo_client[os.getenv('MONGO_DB_NAME')]


    async def add_data(self, request: Request) -> Response:
        if request.has_body:
            json = await request.json()
            json['timestamp'] = datetime.now().timestamp()
        
            coll = self.db[os.getenv('MONGO_COLL')]
            new_msg_id = str(coll.insert_one(json).inserted_id)
        
            if new_msg_id is not None:
                result = {"new_msg_id": new_msg_id}
                status=200
            else:
                result = {"message": "Message not found"}
                status=404

        else:
            result = {"message": "Empty request body"}
            status = 400
        return Response(body=dumps(result), status=status, content_type="application/json")
        

    async def get_data(self, request: Request) -> Response:
        if request.query:
            msg_name = request.query['msg_name']
            
        coll = self.db[os.getenv('MONGO_COLL')]     
        value = coll.find_one({"name": msg_name})
        
        if value is not None:
            value['_id'] = str(value['_id'])
            result = value
            status=200
        else:
            result = {"message": "Not found"}
            status=404

        return Response(body=dumps(result), status=status, content_type="application/json")
