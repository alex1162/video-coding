from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse
from api.first_seminar import Color, DCT, DWT
import subprocess
import json
import os

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
            <h1>Practice2 - MPEPG4 and more endpoints</h1>
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

@app.post("/modify-chroma-subsampling/")
def modify_chroma_subsampling(file: UploadFile, Y: int, Cb: int, Cr: int):
    input_path = f"{MEDIA_FOLDER}/{file.filename}"
    output_path = f"{MEDIA_FOLDER}/chroma_{file.filename}"

    docker = ["docker", "exec", "docker-ffmpeg"]
    if docker:
        # ffmpeg -i input.mp4 -c:v libx264 -vf format=yuv420p output.mp4
        command = docker + ['ffmpeg', '-i', input_path, '-c:v', 'libx264', '-vf', f'format=yuv{Y}{Cb}{Cr}p', output_path]
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(f"Image saved as {output_path}")
            return result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            print(f"Failed to chroma image: {e}")
    else:
        # If no docker is provided, run ffmpeg directly
        command = ['ffmpeg', '-i', input_path, '-c:v', 'libx264', '-vf', f'format={Y}{Cb}{Cr}p', output_path]
        subprocess.run(command)

    return {"status": "success", "output_file": output_path}
 
@app.post("/video-information/")
def get_video_information(file: UploadFile):
    input_path = f"{MEDIA_FOLDER}/{file.filename}"
    
    docker = ["docker", "exec", "docker-ffmpeg"]
    if docker:
    # Command using ffprobe
        command = docker + [ "ffprobe", "-v", "error", "-show_entries", "format=duration,size,bit_rate", "-show_streams", "-select_streams", "v:0",
            "-print_format", "json", input_path]
        try:
            # Run the command and capture the output
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            metadata = json.loads(result.stdout)
            format_info = metadata.get("format", {})
            stream_info = metadata.get("streams", [])[0]  # First video stream

            # Extract relevant details
            extracted_info = {
                "duration": float(format_info.get("duration", 0)),
                "size": int(format_info.get("size", 0)),
                "bit_rate": int(format_info.get("bit_rate", 0)),
                "resolution": f'{stream_info.get("width", "unknown")}x{stream_info.get("height", "unknown")}',
                "frame_rate": eval(stream_info.get("avg_frame_rate", "0/1")),  # Convert "30/1" to 30
            }

            return {"status": "success", "video_info": extracted_info}

        except subprocess.CalledProcessError as e:
            return {"status": "error", "message": str(e)}

@app.post("/process-bbb/")
def process_bbb(file: UploadFile):
    
    input_path = f"{MEDIA_FOLDER}/{file.filename}"
    trimmed_video_path = f"{MEDIA_FOLDER}/trimmed_{file.filename}"
    aac_audio_path = f"{MEDIA_FOLDER}/audio_mono.aac"
    mp3_audio_path = f"{MEDIA_FOLDER}/audio_stereo.mp3"
    ac3_audio_path = f"{MEDIA_FOLDER}/audio.ac3"
    output_mp4_path = f"{MEDIA_FOLDER}/output_combined.mp4"

    docker = ["docker", "exec", "docker-ffmpeg"]
    if docker:
        # Trim the video to 20 seconds
        trim_command = docker + [ "ffmpeg", "-i", input_path, "-t", "20", "-c:v", "libx264", "-c:a", "aac", trimmed_video_path]
        # Export audio as AAC mono
        aac_command = docker + [ "ffmpeg", "-i", trimmed_video_path, "-ac", "1", "-c:a", "aac", aac_audio_path]
        # Export audio as MP3 stereo 
        mp3_command = docker + [ "ffmpeg", "-i", trimmed_video_path, "-ac", "2", "-b:a", "128k", "-c:a", "mp3", mp3_audio_path]
        # Export audio as AC3 codec
        ac3_command = docker + ["ffmpeg", "-i", trimmed_video_path, "-c:a", "ac3", ac3_audio_path]
        # Combine the trimmed video and audio into a single file
        combine_command = docker + ["ffmpeg", "-i", trimmed_video_path, "-i", aac_audio_path, "-map", "0:v:0", "-map", "1:a:0","-c:v", "copy", "-c:a", "aac", output_mp4_path]

        try:
            subprocess.run(trim_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            subprocess.run(aac_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            subprocess.run(mp3_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            subprocess.run(ac3_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            subprocess.run(combine_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

            return {"status": "success", "final_mp4": output_mp4_path }

        except subprocess.CalledProcessError as e:
            return {"status": "error", "message": str(e)}

@app.post("/count-tracks/")
def count_tracks(file: UploadFile):
    input_path = f"{MEDIA_FOLDER}/{file.filename}"

    docker = ["docker", "exec", "docker-ffmpeg"]
    if docker:
        command = docker + [ "ffprobe", "-v", "error", "-select_streams", "v:a", "-show_entries", "stream=index", "-of", "json", input_path] 
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

            metadata = json.loads(result.stdout)
            tracks = metadata.get("streams", [])  # List of all tracks

            return { "status": "success","track_count": len(tracks)}

        except subprocess.CalledProcessError as e:
            return {"status": "error", "message": str(e)}

@app.post("/motion-vectors/")
def motion_vectors(file: UploadFile):

    input_path = f"{MEDIA_FOLDER}/{file.filename}"
    output_path = f"{MEDIA_FOLDER}/macroblocks_{file.filename}"

    docker = ["docker", "exec", "docker-ffmpeg"]
    if docker:
        command = docker + ["ffmpeg", "-flags2", "+export_mvs", "-i", input_path, "-vf", "codecview=mv=pf+bf+bb", output_path]
        try:
            subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

            return { "status": "success", "output_video": output_path,}

        except subprocess.CalledProcessError as e:
            return {"status": "error", "message": str(e)}
        

@app.post("/histogram_YUV/")
def histogram_YUV(file: UploadFile):

    input_path = f"{MEDIA_FOLDER}/{file.filename}"
    output_path = f"{MEDIA_FOLDER}/yuvhistogram_{file.filename}"

    docker = ["docker", "exec", "docker-ffmpeg"]
    if docker:
        command =  docker + [ "ffmpeg", "-i", input_path, "-vf", "split[main][copy];[copy]histogram,format=yuv420p[hist];[main][hist]overlay",
            "-c:v", "libx264", output_path]
        try:
            subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

            return { "status": "success", "output_video": output_path,}

        except subprocess.CalledProcessError as e:
            return {"status": "error", "message": str(e)}

@app.post("/convert-video/")
def convert_videos(file: UploadFile):
       
    input_path = f"{MEDIA_FOLDER}/{file.filename}" 
    vp8_path = f"{MEDIA_FOLDER}/vp8.webm"
    vp9_path = f"{MEDIA_FOLDER}/vp9.webm"
    h265_path = f"{MEDIA_FOLDER}/h265.mp4"
    av1_path = f"{MEDIA_FOLDER}/av1.mkv"

    docker = ["docker", "exec", "docker-ffmpeg"]
    if docker:

        vp8_command =  docker + ["ffmpeg", "-i", input_path, "-c:v", "libvpx", "-b:v", "1M", "-c:a", "libvorbis", vp8_path]
        vp9_command =  docker + ["ffmpeg", "-i", input_path, "-c:v", "libvpx-vp9", "-b:v", "2M", vp9_path]
        h265_command =  docker + ["ffmpeg", "-i", input_path, "-c:v", "libx265", "-crf", "26", "-preset", "fast", "-c:a", "aac", "-b:a", "128k", h265_path]
        #av1_command =  docker + ["ffmpeg", "-i", input_path, "-c:v", "libaom-av1", "-b:v", "2M", av1_path]
        av1_command = docker + ["ffmpeg", "-i", input_path,"-c:v", "libaom-av1", "-b:v", "2M", av1_path]


        subprocess.run(vp8_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text= True)
        subprocess.run(vp9_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(h265_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(av1_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

        return {"status": "success"}


# An encoding ladder is a predefined set of video output specifications designed to accommodate users with varying devices and network conditions.