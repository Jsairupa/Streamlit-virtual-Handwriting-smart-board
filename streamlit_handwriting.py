import streamlit as st
import requests

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

# Google Drive video ID
video_id = "1Pz7DoRdkSHzocEA6BAPwuy8prdE1zp1p"

# Create the embed URL for Google Drive
embed_url = f"https://drive.google.com/file/d/1Pz7DoRdkSHzocEA6BAPwuy8prdE1zp1p/view?usp=drive_link

# Embed the video using an iframe
st.markdown(f"""
<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; border-radius: 10px; margin-bottom: 20px;">
  <iframe src="{embed_url}" 
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" 
    frameborder="0" 
    allow="autoplay; encrypted-media" 
    allowfullscreen>
  </iframe>
</div>
""", unsafe_allow_html=True)

# Alternative direct video link
st.markdown("""
If the embedded video doesn't load, you can [watch the demo video directly on Google Drive](https://drive.google.com/file/d/1Pz7DoRdkSHzocEA6BAPwuy8prdE1zp1p/view?usp=sharing).
""")

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
