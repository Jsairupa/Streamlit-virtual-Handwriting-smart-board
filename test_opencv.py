import streamlit as st

st.title("OpenCV Test")

try:
    import cv2
    st.success(f"OpenCV imported successfully! Version: {cv2.__version__}")
except Exception as e:
    st.error(f"Failed to import OpenCV: {e}")
    
try:
    import mediapipe as mp
    st.success(f"MediaPipe imported successfully! Version: {mp.__version__}")
except Exception as e:
    st.error(f"Failed to import MediaPipe: {e}")