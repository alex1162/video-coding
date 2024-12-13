import unittest
from unittest.mock import patch, Mock
import requests
import streamlit as st
from io import BytesIO

class TestStreamlitApp(unittest.TestCase):
    
    @patch('streamlit.file_uploader')
    @patch('streamlit.image')
    @patch('requests.post')
    def test_image_upload_and_bw_conversion(self, mock_post, mock_image, mock_file_uploader):
        """Test uploading an image and converting it to black & white."""
        # Mock the file uploader to simulate an uploaded image
        mock_file = BytesIO(b"fake_image_data")
        mock_file_uploader.return_value = mock_file

        # Mock the response from the API
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"output_file": "path/to/bw_image.png"}

        # Simulate clicking the "Convert to Black & White" button
        with patch('streamlit.button', side_effect=[True, False]):
            exec(open('api\GUI.py').read(), {'st': st, 'requests': requests})

        # Check that the API was called with the right data
        mock_post.assert_called_once_with(
            "http://127.0.0.1:8000/bw-image/",
            files={"file": mock_file}
        )

    @patch('streamlit.file_uploader')
    @patch('streamlit.video')
    @patch('requests.post')
    def test_video_upload_and_histogram_generation(self, mock_post, mock_video, mock_file_uploader):
        """Test uploading a video and generating YUV histogram."""
        # Mock the file uploader to simulate an uploaded video
        mock_video_file = BytesIO(b"fake_video_data")
        mock_file_uploader.return_value = mock_video_file

        # Mock the response from the API
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"output_video": "path/to/histogram_video.mp4"}

        # Simulate clicking the "Generate YUV Histogram" button
        with patch('streamlit.button', side_effect=[False, True]):
            exec(open('api\GUI.py').read(), {'st': st, 'requests': requests})

        # Check that the API was called with the right data
        mock_post.assert_called_once_with(
            "http://127.0.0.1:8000/histogram_YUV/",
            files={"file": mock_video_file}
        )

if __name__ == "__main__":
    unittest.main()
