import streamlit as st
import requests
from PIL import Image
import io

# Base URL of your FastAPI
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Monster API GUI", layout="centered")

st.title("Monster API GUI")
st.write("Upload an image to apply transformations.")

# File uploader
uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])

# Input fields for resizing
resize_width = st.number_input("Width (px)", min_value=1, value=200)
resize_height = st.number_input("Height (px)", min_value=1, value=200)

if uploaded_file:
    # Display the uploaded image
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    # Convert to Black & White button
    if st.button("Convert to Black & White"):
        # Send the image to the FastAPI backend
        files = {"file": uploaded_file}
        response = requests.post(f"{API_URL}/bw-image/", files=files)
        
        if response.status_code == 200:
            output_file = response.json()["output_file"]
            st.success("Image converted to Black & White!")
            st.image(output_file, caption="Black & White Image")
        else:
            st.error("Failed to process the image. Please try again.")

    # Resize image button
    if st.button("Resize Image"):
        # Send the image and resize dimensions to the FastAPI backend
        files = {"file": uploaded_file}
        data = {"width": resize_width, "height": resize_height}
        response = requests.post(f"{API_URL}/resize-image/", files=files, data=data)
        
        if response.status_code == 200:
            output_file = response.json()["output_file"]
            st.success("Image resized successfully!")
            st.image(output_file, caption="Resized Image")
        else:
            st.error("Failed to resize the image. Please try again.")
