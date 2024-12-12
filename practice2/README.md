# Practice 2. Transcoding

This is a brief manual on how we have performed each task of the practice and the steps to follow to prove its functionality.

**1. Create a new endpoint/feature to convert any input video into VP8, VP9, h265 & AV1.**

To do this practice we won’t start from scratch, we will be taking the previous code and dockers from seminar 2. 

To create a new endpoint to convert an input video into different formats, we used a different ffmpeg command to each of them. The user from the API can choose the video and we proceed running the commands to convert it to the requested formats. 

The AV1 format has been the one which we have had more problems. There are currently three AV1 encoders supported by FFmpeg, but we have used libaom as it's the only one included in our ffmpeg docker (jrottenberg/ffmpeg), which we have found after running the "ffmpeg -codecs" command. As this encoder is not the fastest, we have had to include many parameters, these being:

· *-t 3:* for trimming the video to 3 seconds (longer videos meant much longer waiting time)
· *-crf 50* to modify the constant quality of the conversion, a higher number means worse quality but faster conversion (form 0 to 63).
· *-cpu-used 8* sets how efficient the compression will be. Lower values mean slower encoding with better quality (from 0 to 8).
· *-g 100* can be used to set the maximum keyframe interval. For anything up to 10 seconds and 30 frames per second content one would use -g 300, so we used a lower one for faster conversion.

The main problem we had was that as we were using an older than version 2.0.0 of libaom, we need to add as well *-strict -2*, which we didn't know.

**2. Create a new endpoint/feature to be able to do an encoding ladder.**

**3. Create a GUI.**

----------------------------------------------------------------

To launch the application, after activating the virtual environment (*.venv\Scripts\activate*) and opening the docker desktop app (without closing it), we run the following command to build the docker-compose file inside the docker folder: 

*> cd .\docker*
*> docker-compose up --build*

We then can access the application through our browser, using the URL: *localhost:8000*

To stop running the app, we must press Ctrl+C twice (as the ffmpeg docker is running with a command which allows it to not stop, we must force it to do so).

**IMPORTANT:**
We run the test using pytest.
If using **pytest** (pip install pytest), import by adding a dot before importing the file: import .first_seminar or import .main
If just running with python first_seminar_test.py or test_main.py, remove the dot: import first_seminar or import main
