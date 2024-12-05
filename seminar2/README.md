# Seminar 2. MPEG4 & more Endpoints

This is a brief manual on how we have performed each task of the practice and the steps to follow to prove its functionality.

**1. Create a new endpoint/feature which will let you to modify the resolution (use FFmpeg in the backend).**

To do this practice we will start from the previous practice 1. In this exercice we will use the already created function resize_image, defined in the main.py file in the api folder, with some modifications in order to work.
Then, what we have to do is simply enter the new resolution we want our video to have (defined by its pixel size) and upload the video we want to modify.

**2. Create a new endpoint / feature which will let you to modify the chroma subsampling**

From now on, we will create and implement the endpoints in the main file. To modify the chroma subsampling, we use the ffmpeg command: 
"'ffmpeg', '-i', input_path, '-c:v', 'libx264', '-vf', f'format=yuv{Y}{Cb}{Cr}p', output_path ". 
We modify the command using the entered numbers by the user which is going to be the luma component(Y) and the color components Cb and Cr.

**3. Create a new endpoint / feature which lets you read the video info and print at least 5 relevant data from the video**

To do an endpoint that reads the information of the video and print 5 relevant data we had to use FFMPEG's ffprobe tool in order to extract the data. 
The command ffprobe analyze the video file and retrieve data in JSON format. Then we extract relevant information: the duration(s), the file Size (bytes), the bitrate (average bits per second), the resolution (width x height) and the frame rate (frames per second).

**4. Create another endpoint in order to create a new BBB container and fulfill the specified requirements**

To meet the requirements, we have implemented an endpoint in FastAPI. This endpoint processes an uploaded video file to create a 20-second MP4 container with multiple audio tracks.
First we cut the video to 20 seconds. Then we export the audio as AAC mono, MP3 stereo and the AC3 codec tracks. Finally we package everything in the trimmed video as a single MP4 file.

**5. Create a new endpoint / feature which reads the tracks from an MP4 container, and it’s able to say (deliver an output) of how many tracks does the container contains**

To read the tracks from an MP4 container, we follow the same procedure as in exercise 3, but instead of extracting the duration or the file size, we extract the number of tracks the video file contains. To do so, we extract the stream file and compute its length.

**6. Create a new endpoint / feature which will output a video that will show the macroblocks and the motion vectors**

To obtain the macroblocls and the motion vectors of a video file, we use the ffmpeg command: 
"'ffmpeg', '-flags2', '+export_mvs', '-i', input_path, '-vf', 'codecview=mv=pf+bf+bb', output_path".
This command what does is to show motion vectors as small arrows for each macroblock. The type of motion vector to be drawn comes specified by:
    pf – forward predicted motion vectors of P pictures
    bf – forward predicted motion vectors of B pictures
    bb – backward predicted motion vectors of B pictures

**7. Create a new endpoint / feature which will output a video that will show the YUV histogram**

Now, to obtain the YUV histogram of a video we use the ffmpeg command:
"'ffmpeg', '-i', input_path, '-vf', 'split[main][copy];[copy]histogram,format=yuv420p[hist];[main][hist]overlay',
            '-c:v', 'libx264', output_path"
With this command what we are doing is overlaying the YUV histogram on top of the original video. We first duplicate the video stream into two streams. In the duplicated stream we create the histogram and then we overlay it.

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
