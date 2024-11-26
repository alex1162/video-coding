from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse
from api.first_seminar import Color, DCT, DWT

app = FastAPI()

# SHARED_FOLDER = "/shared"
MEDIA_FOLDER = "/media"

@app.get('/', response_class=HTMLResponse)
def home():
    html = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Home</title>
        </head>
        <body>
            <h1>Practice 1 - API & Dockerization</h1>
            <p> To test the endpoints implemented, go to the API docs page:</p>
            <button onclick="window.location.href='/docs';">Go</button>
        </body>
    </html>
    """
    return html

@app.post("/rgb-to-yuv/")
async def rgb_to_yuv(R: int, G: int, B: int):
    color = Color(R, G, B)
    color.rgb_to_yuv(color.x, color.y, color.z)
    return {"Y": color.x, "U": color.y, "V": color.z}

@app.post("/yuv-to-rgb/")
async def yuv_to_rgb(Y: int, U: int, V: int):
    color = Color(Y, U, V)
    color.yuv_to_rgb(color.x, color.y, color.z)
    return {"R": color.x, "G": color.y, "B": color.z}

@app.post("/bw-image/")
async def bw_image(file: UploadFile):
    input_path = f"{MEDIA_FOLDER}/{file.filename}"
    output_path = f"{MEDIA_FOLDER}/bw_{file.filename}"

    # Convert image to grayscale
    docker = ["docker", "exec", "docker-ffmpeg"]
    Color.bw_image(input_path, output_path, docker)
    return {"status": "success", "output_file": output_path}

@app.post("/resize-image/")
async def resize_image(file: UploadFile, width: int, height: int):
    input_path = f"{MEDIA_FOLDER}/{file.filename}"
    output_path = f"{MEDIA_FOLDER}/resized_{file.filename}"

    # Resize the image
    docker = ["docker", "exec", "docker-ffmpeg"]
    Color.resize_image(input_path, output_path, width, height, docker)
    return {"status": "success", "output_file": output_path}
