# Practice 2. Transcoding

This is a brief manual on how we have performed each task of the practice and the steps to follow to prove its functionality.

**1. Create a new endpoint/feature to convert any input video into VP8, VP9, h265 & AV1.**

To do this practice we won’t start from scratch, we will be taking the previous code and dockers from seminar 2. 
To create a new endpoint to convert an input video into different formats, we used a different ffmpeg command to each of them. The user from the API can choose in which format wants to convert the original video and then, depending on the format chosen we will execute one command or the other. Therefore, we just have to upload the video we want to convert and chose the final format of the video.

**2. Create a new endpoint/feature to be able to do an encoding ladder.**

**3. Create a GUI.**

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
