import streamlit as st
import requests
from PIL import Image
import io
import asyncio


# Base URL of your FastAPI
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Monster API GUI", layout="centered")

st.title("API GUI")
st.write("Upload an image to apply transformation.")

# File uploader
uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Display the uploaded image
    st.image(uploaded_file, use_column_width=True)

    # Convert to Black & White button
    if st.button("Convert to Black & White"):
        # Send the image to the FastAPI backend
        files = {"file": uploaded_file}
        response = requests.post(f"{API_URL}/bw-image/", files=files)
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}

        if response.status_code == 200:
            output_file = response.json()["output_file"]
            st.write(f"Image in the file path: {output_file}")
            st.success("Image converted to Black & White!")
        else:
            st.error("Failed to process the image. Please try again.")

# Video Information
st.header("Video Metadata Extraction")
video_file = st.file_uploader("Upload a Video for Metadata")

if video_file:

    st.video(video_file, format="video/mp4")

    if st.button("Generate YUV Histogram"):
        st.write("This might take a few seconds...")
        files = {"file": video_file}
        response = requests.post(f"{API_URL}/histogram_YUV/", files=files)

        if response.status_code == 200:
            response_data = response.json()
            output_video = response_data["output_video"]
            st.success("YUV Histogram generated successfully!")
            st.write(f"Video in the file path: {output_video}")
        else:
            st.error("Failed to connect to the server. Please try again.")