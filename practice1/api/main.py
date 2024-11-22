from fastapi import FastAPI, UploadFile
from typing import Union
from pathlib import Path
from api.first_seminar import Color, DCT, DWT


app = FastAPI()

SHARED_FOLDER = "/shared"
MEDIA_FOLDER = "/media"

@app.get('/')
def home():
    return "Hello world"

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/bw-image/")
async def bw_image(file: UploadFile):
    input_path = f"{SHARED_FOLDER}/{file.filename}"
    output_path = f"{MEDIA_FOLDER}/bw_{file.filename}"

    # Save uploaded file
    with open(input_path, "wb") as f:
        f.write(await file.read())

    # Convert image to grayscale
    result = Color.bw_image(input_path, output_path)
    return {"status": "success", "output_file": result}

@app.post("/resize-image/")
async def resize_image(file: UploadFile, width: int, height: int):
    input_path = f"{SHARED_FOLDER}/{file.filename}"
    output_path = f"{MEDIA_FOLDER}/resized_{file.filename}"

    # Save uploaded file
    with open(input_path, "wb") as f:
        f.write(await file.read())

    # Resize the image
    result = Color.resize_image(input_path, output_path, (width, height))
    return {"status": "success", "output_file": result}
