import streamlit as st
import os

# Set page config
st.set_page_config(
    page_title="Virtual Handwriting Smart Board",
    page_icon="✏️",
    layout="wide"
)

# App title and description
st.title("Virtual Handwriting Smart Board")
st.markdown("Draw on a virtual canvas using hand gestures captured by your webcam.")

# Video demo section
st.header("Project Demo")

# Get the video filename - using the actual filename from your repository
video_file = "6FC267BB-C393-4F3A-83A6-6962A9196B15.mov"

# Check if the video file exists and display it
if os.path.exists(video_file):
    # Open the video file
    video_bytes = open(video_file, 'rb').read()
    
    # Display the video with controls
    st.video(video_bytes)
else:
    st.error(f"Video file not found: {video_file}")

# Project description
st.header("Project Overview")
st.markdown("""
This project implements a real-time handwriting recognition system using computer vision and deep learning.
The system tracks hand movements using a webcam and converts them into digital drawings.

### Features
- Track hand movements using a webcam
- Recognize different hand gestures for drawing, erasing, and clearing
- Convert hand movements into digital drawings
- Save drawings as PNG files
- Demo mode for environments without camera access

### Technologies Used
- Python
- OpenCV for image processing
- MediaPipe for hand landmark detection
- Streamlit for the web interface
- NumPy for numerical operations
""")

# GitHub repository link (update with your actual repository)
st.markdown("### Source Code")
st.markdown("[GitHub Repository](https://github.com/Jsairupa/virtual-handwriting)")

# Add sidebar information
with st.sidebar:
    st.header("Controls")
    
    st.markdown("### Gesture Controls")
    st.markdown("""
    - **Index finger up**: Draw on canvas
    - **Index + Middle fingers up**: Erase
    - **All fingers up**: Clear canvas
    """)
    
    st.markdown("---")
    
    st.markdown("### About the Developer")
    st.markdown("""
    **Sai Rupa Jhade**
    
    Data Science & Computer Vision Enthusiast
    
    [Portfolio](https://jsairupa.github.io/portfolio.html)
    """)
