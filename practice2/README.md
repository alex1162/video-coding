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
We have created a new endpoint, similar to the previous one, using the ffmpeg command to do so. For this endpoint we allow the user to enter the resolution and bitrate of the ouput video.

**3. Create a GUI.**

In this case, we chose to use a Streamlit app because one of our group members had prior experience with it in another subject, which made it easier to work with. We implemented two of the endpoints we had already created into the app.

To install streamil we use:
pip install streamlit
To run the application, use the following command in your terminal:
*>streamlit run GUI.py

The first endpoint allows you to convert an image to Black & White. After selecting an image, the app displays the original image. Once you apply the Black & White transformation, the new image is saved to the output path.
The second endpoint works with videos. You start by selecting a video, which is then displayed in the app. After processing, the video with the YUV histogram overlay is saved to your output path.

We tried modifying the docker compose and creating a new docker for streamlit, but after doing that, we have found some problems making the ffmpeg docker and the streamlit communicate. Hence, due to time constrains we have opted on skipping this implementation and running the GUI on streamlit separately.

**4. Improving our code with AI**
We have created a new file called test_GUI.py which has unit tests for the GUI.py file. We have also thought on enhancing our GUI adding more endpoints but we haven't had time. We used AI to reduce lines on our code for the GUI and unit tests.

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
