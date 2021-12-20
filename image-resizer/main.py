import uvicorn
import os
from io import BytesIO
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.datastructures import UploadFile
from fastapi.responses import Response
from fastapi.params import File
from starlette.responses import StreamingResponse
from db import Database
from cv2 import imdecode, resize, IMREAD_COLOR, imencode
import numpy as np


app = FastAPI(title="Image resizer")
db = Database()


@app.get("/get/{id}")
async def get(id: int, mult: float):
    try:
        nparr = db.get(id)
        img = imdecode(nparr, IMREAD_COLOR)
        dsize = (int(img.shape[0] * mult), int(img.shape[1] * mult))
        resized = resize(img, dsize)
        res, enc_img = imencode(".jpeg", resized)
    except Exception as e:
        raise HTTPException(404, str(e))
    return StreamingResponse(content=BytesIO(enc_img.tobytes()), media_type="image/png")


@app.post("/add")
async def add(image: UploadFile = File(...)):
    try:
        content = await image.read()
        nparr = np.fromstring(content, np.uint8)
        id = db.add(nparr)
    except Exception as e:
        raise HTTPException(404, str(e))
    return {"id": id}


@app.delete("/delete/{id}")
async def delete(id: int):
    try:
        db.delete(id)
    except Exception as e:
        raise HTTPException(404, str(e))


if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv('HOST'), port=os.getenv('PORT'))
