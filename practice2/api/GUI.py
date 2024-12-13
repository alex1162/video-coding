import streamlit as st
import requests
from PIL import Image

# Base URL of your FastAPI
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Monster API GUI", layout="wide")

st.title("Monster API GUI")
st.write("Upload an image or video to apply transformations.")

# File uploader
uploaded_file = st.file_uploader("Choose a file (image or video)", type=["png", "jpg", "jpeg", "mp4", "avi", "mov"])

# Input fields for resizing
resize_width = st.number_input("Width (px)", min_value=1, value=200)
resize_height = st.number_input("Height (px)", min_value=1, value=200)

if uploaded_file:
    # Detect file type
    file_type = uploaded_file.type
    st.write(f"Uploaded file type: {file_type}")

    # Show file preview if it's an image
    if file_type.startswith("image"):
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        # Convert to Black & White
        if st.button("Convert to Black & White"):
            files = {"file": uploaded_file}
            response = requests.post(f"{API_URL}/bw-image/", files=files)
            
            if response.status_code == 200:
                output_file = response.json()["output_file"]
                st.success("Image converted to Black & White!")
                st.image(output_file, caption="Black & White Image")
            else:
                st.error("Failed to process the image. Please try again.")

        # Resize image
        if st.button("Resize Image"):
            files = {"file": uploaded_file}
            data = {"width": resize_width, "height": resize_height}
            response = requests.post(f"{API_URL}/resize-image/", files=files, data=data)
            
            if response.status_code == 200:
                output_file = response.json()["output_file"]
                st.success("Image resized successfully!")
                st.image(output_file, caption="Resized Image")
            else:
                st.error("Failed to resize the image. Please try again.")

    # Process video for YUV histogram
    elif file_type.startswith("video"):
        st.video(uploaded_file, format="video/mp4", start_time=0)
        
        if st.button("Generate YUV Histogram"):
            files = {"file": uploaded_file}
            response = requests.post(f"{API_URL}/histogram_YUV/", files=files)
            
            if response.status_code == 200:
                output_video = response.json()["output_video"]
                st.success("YUV Histogram generated successfully!")
                st.video(output_video, format="video/mp4", start_time=0)
            else:
                st.error("Failed to generate YUV Histogram. Please try again.")
