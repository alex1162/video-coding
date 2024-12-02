# Practice 1. API & DOCKERIZATION

This is a brief manual on how we have performed each task of the practice and the steps to follow to prove its functionality.

**1.Create a new endpoint/feature which will let you to modify the resolution (use FFmpeg in the backend).**

To do this practice we will use the previous practice 1. In this exercice we will use the already created function resize_image with some modifications in order to work.

Here we will **create** a virtual environment:

*> python -m venv .venv*

And then **activate** it:

*> .venv\Scripts\activate (windows, PowerShell)*

*> source .venv/bin/activate (linux)*

**2. Put ffmpeg inside a Docker**
We create a new dockerfile called Dockerfile_ffmpeg. We get ffmpeg from *jrottenberg/ffmpeg:latest*, which already prepares a minimalist Docker image with FFmpeg. As we will need to run continuously this docker in the background (to be able to call the functions that depend on it), we add a command to do so. We also add the directory of the media folder, which will be shared with the api docker and will be used to store the media we will use. 

**3. Include all your previous work inside the new API. Use the help of any AI tool to adapt the code and the unit tests**
Instead of using the python file from seminar 1, we duplicate it and bring it to the api folder. Here adapt the code of some functinos so that we can run them from the api docker, which uses the ffmpeg docker too. This basically means that we were calling some ffmpeg commands before which will need to be modified so that they can be called from the api docker (in our case, we had to add: "docker", "exec", "docker-ffmpeg" at the beginning of the commands). We also adapt the test file *first_seminar_test.py* updating the folder where the media is stored. We run the test using pytest(*).

**4. Create at least 2 endpoints which will process some actions from the previous S1**
We have created the *main.py* file, which defines a FastAPI application with several endpoints. The API includes a home route that serves a simple HTML page with a link to the API documentation. We have added two color conversion endpoints: one for converting RGB values to YUV (/rgb-to-yuv/) and another for converting YUV back to RGB (/yuv-to-rgb/). Additionally, we added two endpoints for image processing: one for converting images to black and white (/bw-image/) and another for resizing images (/resize-image/). Both image processing endpoints work with files uploaded through the API and use Docker to run the ffmpeg container for the media manipulation.

**5. Use docker-compose to launch both and make them interact (i.e., you have a method for conversion, you launch your API and it will call the FFMPEG docker)**
We finally create the docker-compose file, which allows both the API and ffmpeg containers to communicate through shared volumes and the Docker network. By defining the api and ffmpeg services in the same docker-compose file, it automatically places them on a shared network, allowing them to access each other by their service names. The api container can execute commands (like docker exec) within the ffmpeg container, which is enabled by mounting the Docker socket (/var/run/docker.sock). This provides the api container with the necessary permissions to control Docker on the host. Finally, as mentioned previously, the shared /media volume ensures both containers have access to the same media files, enabling file transfers and manipulation between the services. 

To launch the application, after creating the virtual environment (described in 1.), we run the following command to build the docker-compose file inside the docker folder: 

*> cd .\docker*
*> docker-compose up --build*

It's important to have installed the docker desktop app on our computer and keep the program opened when running this command. We then can access the application through our browser, using the URL: *localhost:8000*

**(*)IMPORTANT:**
If using **pytest** (pip install pytest), import by adding a dot before importing the file: import .first_seminar or import .main
If just running with python first_seminar_test.py or test_main.py, remove the dot: import first_seminar or import main
