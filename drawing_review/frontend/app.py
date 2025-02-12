import streamlit as st
import sys
import os
import tempfile
import cv2
import numpy as np
# os.path.dirname(__file__) → Gets the directory of app.py (frontend/).
current_dir = os.path.dirname(__file__)
# os.path.join(..., "../..") → Moves two levels up, reaching drawing_review/.
absolute_path = os.path.abspath(os.path.join(current_dir, "../"))
# Get the absolute path of the project root directory
sys.path.append(absolute_path)

from backend.services.image_processing import process_images

# Set page background color
st.markdown(
    """
    <style>
        .stApp {
            background-color: black;
            color: white;
        }
        .stFileUploader label {
            font-size: 20px !important;
            font-weight: bold;
            color: #FFDD44;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit UI
st.title("2D Drawing Review Tool")
st.write("Upload two images to compare and highlight differences.")

# Upload files
old_file = st.file_uploader("...............Upload old drawing...............", type=["jpg", "png", "jpeg"])
new_file = st.file_uploader("...............Upload new drawing...............", type=["jpg", "png", "jpeg"])

if old_file and new_file:

    # Save uploaded files temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_old:
        temp_old.write(old_file.read())
        old_path = temp_old.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_new:
        temp_new.write(new_file.read())
        new_path = temp_new.name

    # Process images
    st.write("Processing images...")
    result = process_images(old_path, new_path)

    # Convert to display format
    result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

    # Display both images side by side
    col1, col2 = st.columns(2)
    with col1:
        st.image(old_path, caption="Old Drawing", use_container_width=True)
    with col2:
        # Show result
        st.image(result_rgb, caption="Differences Highlighted", use_container_width=True)
    

    # Cleanup temp files
    os.remove(old_path)
    os.remove(new_path)
