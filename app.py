import cv2
import mediapipe as mp
from controller import Controller
import webbrowser

cap = cv2.VideoCapture(0)
# open maps directly
webbrowser.open('https://www.google.com/maps/@?api=1&map_action=map&basemap=satellite')

mpHands = mp.solutions.hands
hands = mpHands.Hands( # add parameters to the hands module
      max_num_hands=1, # limit the number of hands to 1 to improve performance
      min_detection_confidence=0.80, 
      min_tracking_confidence=0.80
   )  
mpDraw = mp.solutions.drawing_utils

frame_skip = 2  # Continue skipping frames as before.
frame_counter = 0

# New resolution (width, height)
desired_width = 640
desired_height = 360

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Resize the frame
    img = cv2.resize(img, (desired_width, desired_height))

    frame_counter += 1
    if frame_counter % frame_skip == 0:
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            Controller.hand_Landmarks = results.multi_hand_landmarks[0]
            mpDraw.draw_landmarks(img, Controller.hand_Landmarks, mpHands.HAND_CONNECTIONS)
            
            # Your gesture processing logic
            Controller.update_fingers_status()
            Controller.cursor_moving()
            Controller.detect_zoomming()
            Controller.detect_clicking()
            Controller.detect_dragging()

    cv2.imshow('Hand Tracker', img)
    if cv2.waitKey(5) & 0xFF == 27:
        break
    