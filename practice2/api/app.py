import streamlit as st
import asyncio

from main import rgb_to_yuv, yuv_to_rgb, bw_image, resize_image, get_video_information

# Streamlit App
st.title("Media Processing Application")

# RGB to YUV
st.header("RGB to YUV Conversion")
R = st.number_input("Red (R)", min_value=0, max_value=255, value=0)
G = st.number_input("Green (G)", min_value=0, max_value=255, value=0)
B = st.number_input("Blue (B)", min_value=0, max_value=255, value=0)
if st.button("Convert to YUV"):
    yuv_result = asyncio.run(rgb_to_yuv(R, G, B))
    st.write("YUV Result:", yuv_result)

# YUV to RGB
st.header("YUV to RGB Conversion")
Y = st.number_input("Luminance (Y)", min_value=0, max_value=255, value=0)
U = st.number_input("Chroma Blue (U)", min_value=0, max_value=255, value=0)
V = st.number_input("Chroma Red (V)", min_value=0, max_value=255, value=0)
if st.button("Convert to RGB"):
    rgb_result = asyncio.run(yuv_to_rgb(Y, U, V))
    st.write("RGB Result:", rgb_result)

# Grayscale Conversion
st.header("Grayscale Image Conversion")
bw_file = st.file_uploader("Upload an Image for Grayscale Conversion")
if bw_file and st.button("Convert to Grayscale"):
    # Assuming bw_image accepts file-like objects
    result = asyncio.run(bw_image(bw_file.name))
    st.write("Conversion Result:", result)

# Video Information
st.header("Video Metadata Extraction")
video_file = st.file_uploader("Upload a Video for Metadata")
if video_file and st.button("Extract Metadata"):
    metadata = asyncio.run(get_video_information(video_file))
    st.write("Video Metadata:", metadata)
