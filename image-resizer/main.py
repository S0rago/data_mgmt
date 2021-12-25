import uvicorn
import os
from io import BytesIO
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.datastructures import UploadFile
from fastapi.params import File, Form
from starlette.responses import StreamingResponse
from db import Database
from cv2 import imdecode, resize, IMREAD_COLOR, imencode
import numpy as np

app = FastAPI(title="Image resizer")
db = Database()
root_api = os.getenv("BASE_API", '/images')


@app.get(root_api + "/getbyid/{id}")
async def getbyid(id: int):
    try:
        file = db.getbyid(id)
        image = file.content
    except Exception as e:
        raise HTTPException(404, str(e))
    return StreamingResponse(content=BytesIO(image), media_type="image/png")


@app.get(root_api + "/getbyname/{name}")
async def getbyname(name: str):
    try:
        file = db.getbyname(name)
        image = file.content
    except Exception as e:
        raise HTTPException(404, str(e))
    return StreamingResponse(content=BytesIO(image), media_type="image/png")


@app.get(root_api + "/getsize/{id}")
async def getsize(id: int):
    try:
        file = db.getbyid(id)
        image = file.content
    except Exception as e:
        raise HTTPException(404, str(e))
    return {"file_size": len(image)}


@app.get(root_api + "/modify/{id}")
async def modify(id: int, mult: float):
    try:
        file = db.getbyid(id)
        img = imdecode(np.frombuffer(file.content, dtype=np.uint8), IMREAD_COLOR)
        dsize = (int(img.shape[0] * mult), int(img.shape[1] * mult))
        resized = resize(img, dsize)
        res, enc_img = imencode(".jpeg", resized)
    except Exception as e:
        raise HTTPException(404, str(e))
    return StreamingResponse(content=BytesIO(enc_img.tobytes()), media_type="image/png")


@app.post(root_api + "/add")
async def add(filename: str = Form(...), image: UploadFile = File(...)):
    try:
        content = await image.read()
        id = db.add(filename, content)
    except Exception as e:
        raise HTTPException(404, str(e))
    return {"id": id}


@app.delete(root_api + "/delete/{id}")
async def delete(id: int):
    try:
        db.delete(id)
    except Exception as e:
        raise HTTPException(404, str(e))
    return {"deleted": id}


if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv('HOST', 'localhost'),
                port=int(os.getenv('PORT', '6969')))
