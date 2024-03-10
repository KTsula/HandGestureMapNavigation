import cv2
import mediapipe as mp
from controller import Controller
import webbrowser

# open maps directly
webbrowser.open('https://www.google.com/maps')

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

frame_skip = 3  # Skip every 3 frames. Adjust this number as needed.
frame_counter = 0  # Frame counter

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    frame_counter += 1
    if frame_counter % frame_skip == 0:  # Process frame if it's the n-th frame
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            Controller.hand_Landmarks = results.multi_hand_landmarks[0]
            mpDraw.draw_landmarks(img, Controller.hand_Landmarks, mpHands.HAND_CONNECTIONS)
            
            Controller.update_fingers_status()
            Controller.cursor_moving()
            Controller.detect_scrolling()
            Controller.detect_zoomming()
            Controller.detect_clicking()
            Controller.detect_dragging()

    cv2.imshow('Hand Tracker', img)
    if cv2.waitKey(5) & 0xFF == 27:
        break

# DragDrop
# rightclick
# leftclick
# doubleclick
# scroll up
# scroll down
# Zoom in 
# Zoom out