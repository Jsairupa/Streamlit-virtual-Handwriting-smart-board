import streamlit as st
import numpy as np
import cv2
import time
from PIL import Image
import io

# Set page config
st.set_page_config(
    page_title="Virtual Handwriting Smart Board",
    page_icon="✏️",
    layout="wide"
)

# App title and description
st.title("Virtual Handwriting Smart Board")
st.markdown("Draw on a virtual canvas using hand gestures captured by your webcam.")

# Initialize session state variables
if 'img_canvas' not in st.session_state:
    st.session_state.img_canvas = np.zeros((480, 640, 3), np.uint8)
if 'demo_running' not in st.session_state:
    st.session_state.demo_running = False
if 'demo_speed' not in st.session_state:
    st.session_state.demo_speed = 1.0
if 'drawing_color' not in st.session_state:
    st.session_state.drawing_color = (255, 255, 255)
if 'brush_size' not in st.session_state:
    st.session_state.brush_size = 5
if 'demo_mode' not in st.session_state:
    st.session_state.demo_mode = 0  # 0: Draw, 1: Erase, 2: Clear
if 'demo_time' not in st.session_state:
    st.session_state.demo_time = time.time()
if 'hand_position' not in st.session_state:
    st.session_state.hand_position = (320, 240)
if 'prev_position' not in st.session_state:
    st.session_state.prev_position = None

# Sidebar for controls
with st.sidebar:
    st.header("Demo Controls")
    
    # Start/Stop demo
    if st.button("Start Demo" if not st.session_state.demo_running else "Stop Demo"):
        st.session_state.demo_running = not st.session_state.demo_running
        st.session_state.demo_time = time.time()
        if st.session_state.demo_running:
            st.session_state.img_canvas = np.zeros((480, 640, 3), np.uint8)
    
    # Demo speed
    st.session_state.demo_speed = st.slider("Demo Speed", 0.5, 2.0, 1.0, 0.1)
    
    # Color picker
    color_options = {
        "White": (255, 255, 255),
        "Red": (0, 0, 255),  # BGR format
        "Green": (0, 255, 0),
        "Blue": (255, 0, 0),
        "Yellow": (0, 255, 255)
    }
    selected_color = st.selectbox("Drawing Color", list(color_options.keys()))
    st.session_state.drawing_color = color_options[selected_color]
    
    # Brush size
    st.session_state.brush_size = st.slider("Brush Size", 1, 20, 5)
    
    # Clear canvas button
    if st.button("Clear Canvas"):
        st.session_state.img_canvas = np.zeros((480, 640, 3), np.uint8)
    
    st.markdown("---")
    
    st.header("Gesture Controls")
    st.markdown("""
    In the real application:
    - **Index finger up**: Draw on canvas
    - **Index + Middle fingers up**: Erase
    - **All fingers up**: Clear canvas
    """)

# Main app layout
col1, col2 = st.columns(2)

with col1:
    st.header("Camera Feed (Simulated)")
    camera_placeholder = st.empty()

with col2:
    st.header("Drawing Canvas")
    canvas_placeholder = st.empty()
    
    # Save button
    if st.button("Save Drawing"):
        canvas_img = Image.fromarray(st.session_state.img_canvas)
        buf = io.BytesIO()
        canvas_img.save(buf, format="PNG")
        st.download_button(
            label="Download Drawing",
            data=buf.getvalue(),
            file_name="virtual_drawing.png",
            mime="image/png"
        )

# Function to update the demo animation
def update_demo():
    # Create a blank frame for the camera view
    camera_frame = np.zeros((480, 640, 3), np.uint8)
    
    # Current time adjusted by speed
    current_time = (time.time() - st.session_state.demo_time) * st.session_state.demo_speed
    
    # Determine demo mode based on time
    mode_duration = 5  # seconds per mode
    mode_time = current_time % (mode_duration * 3)
    
    if mode_time < mode_duration:
        # Drawing mode
        st.session_state.demo_mode = 0
        mode_text = "DRAWING MODE"
        hand_color = (0, 255, 0)  # Green for drawing
    elif mode_time < mode_duration * 2:
        # Erasing mode
        st.session_state.demo_mode = 1
        mode_text = "ERASING MODE"
        hand_color = (0, 0, 255)  # Red for erasing
    else:
        # Clear mode
        st.session_state.demo_mode = 2
        mode_text = "CLEAR MODE"
        hand_color = (255, 255, 0)  # Cyan for clearing
        # Clear canvas at the beginning of clear mode
        if mode_time - mode_duration * 2 < 0.1:
            st.session_state.img_canvas = np.zeros((480, 640, 3), np.uint8)
    
    # Add text showing the current mode
    cv2.putText(camera_frame, mode_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # Simulate hand movement
    t = current_time * 0.5
    x = int(320 + 200 * np.sin(t))
    y = int(240 + 150 * np.cos(t * 1.3))
    st.session_state.hand_position = (x, y)
    
    # Draw simulated hand
    if st.session_state.demo_mode == 0:
        # Drawing mode - show index finger only
        cv2.circle(camera_frame, (x, y), 15, hand_color, -1)
        # Draw a line from wrist to finger
        wrist_x, wrist_y = int(320 + 50 * np.sin(t)), int(400 + 20 * np.cos(t))
        cv2.line(camera_frame, (wrist_x, wrist_y), (x, y), hand_color, 5)
        
        # Draw on canvas
        if st.session_state.prev_position:
            cv2.line(
                st.session_state.img_canvas, 
                st.session_state.prev_position, 
                (x, y), 
                st.session_state.drawing_color, 
                st.session_state.brush_size
            )
        st.session_state.prev_position = (x, y)
        
    elif st.session_state.demo_mode == 1:
        # Erasing mode - show two fingers
        cv2.circle(camera_frame, (x, y), 15, hand_color, -1)
        cv2.circle(camera_frame, (x+30, y+10), 15, hand_color, -1)
        # Draw a line from wrist to fingers
        wrist_x, wrist_y = int(320 + 50 * np.sin(t)), int(400 + 20 * np.cos(t))
        cv2.line(camera_frame, (wrist_x, wrist_y), (x, y), hand_color, 5)
        
        # Erase from canvas
        cv2.circle(
            st.session_state.img_canvas, 
            (x, y), 
            st.session_state.brush_size * 3, 
            (0, 0, 0), 
            -1
        )
        st.session_state.prev_position = None
        
    else:
        # Clear mode - show all fingers
        cv2.circle(camera_frame, (x, y), 15, hand_color, -1)
        cv2.circle(camera_frame, (x+30, y+10), 15, hand_color, -1)
        cv2.circle(camera_frame, (x+50, y+5), 15, hand_color, -1)
        cv2.circle(camera_frame, (x+70, y+15), 15, hand_color, -1)
        cv2.circle(camera_frame, (x+90, y+30), 15, hand_color, -1)
        # Draw a line from wrist to fingers
        wrist_x, wrist_y = int(320 + 50 * np.sin(t)), int(400 + 20 * np.cos(t))
        cv2.line(camera_frame, (wrist_x, wrist_y), (x, y), hand_color, 5)
        
        st.session_state.prev_position = None
    
    # Draw hand landmarks
    for i in range(21):
        # Simulate 21 hand landmarks with slight variations
        lm_x = x + int(np.sin(i * 0.3 + t) * 10)
        lm_y = y + int(np.cos(i * 0.3 + t) * 10)
        cv2.circle(camera_frame, (lm_x, lm_y), 2, (255, 255, 255), -1)
    
    # Draw hand connections
    cv2.putText(camera_frame, "Hand Tracking Active", (20, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
    
    # Display frames
    camera_placeholder.image(camera_frame, channels="BGR", use_column_width=True)
    canvas_placeholder.image(st.session_state.img_canvas, channels="BGR", use_column_width=True)

# Project description
st.markdown("---")
st.header("Project Overview")
st.markdown("""
This project implements a real-time handwriting recognition system using computer vision and deep learning.
The system tracks hand movements using a webcam and converts them into digital drawings.

### How It Works

1. **Hand Detection**: The application uses MediaPipe to detect and track hand landmarks in real-time.
2. **Gesture Recognition**: By analyzing the positions of finger landmarks, the system recognizes different gestures.
3. **Drawing Implementation**: The recognized gestures are translated into drawing actions on a virtual canvas.

### Technologies Used
- Python
- OpenCV for image processing
- MediaPipe for hand landmark detection
- Streamlit for the web interface
- NumPy for numerical operations
""")

# GitHub repository link
st.markdown("### Source Code")
st.markdown("[GitHub Repository](https://github.com/Jsairupa/virtual-handwriting)")

# Run the demo update in a loop if demo is running
if st.session_state.demo_running:
    update_demo()
    st.experimental_rerun()
else:
    # Show static frames when demo is not running
    camera_frame = np.zeros((480, 640, 3), np.uint8)
    cv2.putText(camera_frame, "DEMO PAUSED", (220, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(camera_frame, "Click 'Start Demo' to begin", (160, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
    
    camera_placeholder.image(camera_frame, channels="BGR", use_column_width=True)
    canvas_placeholder.image(st.session_state.img_canvas, channels="BGR", use_column_width=True)
