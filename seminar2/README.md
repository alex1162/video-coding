# Seminar 2. MPEG4 & more Endpoints

This is a brief manual on how we have performed each task of the practice and the steps to follow to prove its functionality.

**1. Create a new endpoint/feature which will let you to modify the resolution (use FFmpeg in the backend).**

To do this practice we will start from the previous practice 1. In this exercice we will use the already created function resize_image, defined in the main.py file in the api folder, with some modifications in order to work.
Then, what we have to do is simply enter the new resolution we want our video to have (defined by its pixel size) and upload the video.

**2. Create a new endpoint / feature which will let you to modify the chroma subsampling**

From now on, we will create and implement the endpoints in the main file. To modify the chroma subsampling, we use the ffmpeg command: 
"'ffmpeg', '-i', input_path, '-c:v', 'libx264', '-vf', f'format=yuv{Y}{Cb}{Cr}p', output_path ". 
We modify the command using the entered numbers by the user which is sgoing to be the luma component(Y) and the color components Cb and Cr.

**3. Create a new endpoint / feature which lets you read the video info and print at least 5 relevant data from the video**

To do an endpoint with that reads the information of the video and print 5 relevant data we had to use FFMPEG's ffprobe tool in order to extract the data. 
The command ffprobe analyze the video file and retrieve data in JSON format. Then we extract elevant information: the duration(s), the file Size (bytes), the bitrate (average bits per second), the resolution (width x height) and the frame rate (frames per second).

**4. Create another endpoint in order to create a new BBB container and fulfill the specified requirements**

To meet the requirements, we have implemented an endpoint in FastAPI. This endpoint processes an uploaded video file to create a 20-second MP4 container with multiple audio tracks.
First we cut the video to 20 seconds. Then we export the audio as AAC mono, MP3 stereo and the AC3 codec tracks. Finally we package everything in the trimmed video as a single MP4 file.

**5. Create a new endpoint / feature which reads the tracks from an MP4 container, and it’s able to say (deliver an output) of how many tracks does the container contains**



**6. Create a new endpoint / feature which will output a video that will show the macroblocks and the motion vectors**



**7. Create a new endpoint / feature which will output a video that will show the YUV histogram**



----------------------------------------------------------------

To launch the application, after creating the virtual environment, we run the following command to build the docker-compose file inside the docker folder: 

*> cd .\docker*
*> docker-compose up --build*

It's important to have installed the docker desktop app on our computer and keep the program opened when running this command. We then can access the application through our browser, using the URL: *localhost:8000*

To stop running the app, we must press Ctrl+C twice (as the ffmpeg docker is running with a command which allows it to not stop, we must force it to do so).

**IMPORTANT:**
We run the test using pytest.
If using **pytest** (pip install pytest), import by adding a dot before importing the file: import .first_seminar or import .main
If just running with python first_seminar_test.py or test_main.py, remove the dot: import first_seminar or import main
