import streamlit as st
import sys
import os
import tempfile
import cv2
import numpy as np

current_dir = os.path.dirname(__file__)
absolute_path = os.path.abspath(os.path.join(current_dir, "../"))
sys.path.append(absolute_path)

from backend.services.image_processing import process_images

# Set page background color and custom styling including download buttons
st.markdown(
    """
    <style>
        /* Entire app background in black with an inset shadow for a "deep" look */
        .stApp {
            background-color: #000000;
            color: #FFFFFF;
            box-shadow: inset 0 0 30px rgba(0, 0, 0, 0.8);
        }
        /* Title styling */
        h1, h2, h3, h4, h5, h6 {
            color: #FFDD44;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
        }
        /* "Floating" style container for the file uploader */
        .stFileUploader {
            background-color: #222222;
            border: 2px solid #444444;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.8);
            margin-bottom: 20px;
        }
        .stFileUploader label {
            font-size: 20px !important;
            font-weight: bold;
            color: #FFDD44;
            text-align: center;
        }
        .stFileUploader div[data-testid="stFileUploadDropzone"] {
            background-color: #333333;
            border: 2px dashed #FFDD44;
            border-radius: 10px;
            padding: 20px;
            transition: background-color 0.3s ease;
        }
        .stFileUploader div[data-testid="stFileUploadDropzone"]:hover {
            background-color: #444444;
        }
        .upload-heading {
            color: #FFDD44;
            font-size: 22px;
            font-weight: bold;
            text-align: center;
            margin: 20px 0 5px 0;
            background: #222222;
            padding: 10px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.8);
        }
        /* Custom styling for download buttons */
        .stDownloadButton > button {
            background-color: #FFDD44;
            color: #000000;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            margin: 8px 0;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit UI
st.title("2D Drawing Review Tool")
st.write("Upload two images to compare and highlight differences.")

# Attractive heading + file uploader for OLD drawing
st.markdown('<div class="upload-heading">Upload Old Drawing</div>', unsafe_allow_html=True)
old_file = st.file_uploader(
    "Select Old Drawing", 
    type=["jpg", "png", "jpeg"],
    label_visibility="collapsed",
    key="old_file_uploader"
)

# Attractive heading + file uploader for NEW drawing
st.markdown('<div class="upload-heading">Upload New Drawing</div>', unsafe_allow_html=True)
new_file = st.file_uploader(
    "Select New Drawing", 
    type=["jpg", "png", "jpeg"],
    label_visibility="collapsed",
    key="new_file_uploader"
)

# Once both files are uploaded, process them
if old_file and new_file:
    # Get file bytes
    old_bytes = old_file.getvalue()
    new_bytes = new_file.getvalue()
    
    # Save bytes to temporary files for processing
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_old:
        temp_old.write(old_bytes)
        old_path = temp_old.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_new:
        temp_new.write(new_bytes)
        new_path = temp_new.name

    st.write("Processing images...")

    # Process images (difference detection)
    result = process_images(old_path, new_path)
    result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

    # Display both images side by side
    col1, col2 = st.columns(2)
    with col1:
        st.image(old_bytes, caption="Old Drawing", use_container_width=True)
    with col2:
        st.image(result_rgb, caption="Differences Highlighted", use_container_width=True)

    # Encode processed image to PNG bytes for download
    _, processed_buffer = cv2.imencode('.png', result_rgb)
    processed_bytes = processed_buffer.tobytes()

    # Display download buttons
    st.download_button(
        label="Download Processed Image",
        data=processed_bytes,
        file_name="processed_image.png",
        mime="image/png"
    )
    st.download_button(
        label="Download Old Drawing",
        data=old_bytes,
        file_name="old_drawing.jpg",
        mime="image/jpeg"
    )
