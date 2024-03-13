# Hand Gesture Map Navigation

## Introduction

This project presents an innovative way to navigate maps using hand gestures. Utilizing advanced gesture recognition technology, it offers an intuitive and interactive approach to map navigation.

## Project Description

Hand Gesture Map Navigation is a Python-based application that allows users to control and navigate maps through simple hand gestures. The application uses a webcam to recognize specific hand movements, translating them into navigation commands on digital maps.

## Requirements

To use this application, the following libraries need to be installed:

- OpenCV
- Mediapipe
- PyAutoGUI

Install these libraries using pip:

`pip install opencv-python mediapipe pyautogui`

Or, install from `requirements.txt`:

`pip install -r requirements.txt`

## Usage Instructions

After installing the required libraries, run the `app.py` file in a Python environment with an active webcam. The application will start and you can navigate the map using the defined hand gestures.

## Hand Gestures for Map Navigation

- **Move Cursor**: Raise all fingers and move your hand to navigate the map.
- **Zoom In**: Pinch your fingers together to zoom in on the map.
- **Zoom Out**: Spread your fingers apart to zoom out on the map.
- **Scroll**: Use a vertical or horizontal hand motion to scroll through the map.
- **Right Click**: Raise your index finger while keeping the other fingers closed.
- **Left Click**: Raise your index finger while keeping the other fingers closed.
- **Double Click**: Raise your index and middle finger while keeping the other fingers closed.
- **Freeze Cursor**: Close your thumb and raise all other fingers together to freeze the cursor.

## How it Works

The application uses the Mediapipe library for real-time hand tracking and the PyAutoGUI library for translating these gestures into map navigation commands.

## Limitations

Currently, the application supports single-hand gestures and may have reduced performance in low-light conditions.

---

Hand Gesture Map Navigation offers a unique and engaging way to interact with digital maps, enhancing the user experience through natural and intuitive controls.
