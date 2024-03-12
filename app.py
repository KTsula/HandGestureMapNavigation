import cv2
from controller import HandController
from hand_detector import HandDetector
import webbrowser


def main():
    cap = cv2.VideoCapture(0)
    webbrowser.open('https://www.google.com/maps/@?api=1&map_action=map&basemap=satellite')

    hand_detector = HandDetector()

    frame_skip = 2
    frame_counter = 0
    desired_width = 640
    desired_height = 360

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = cv2.resize(img, (desired_width, desired_height))

        frame_counter += 1
        if frame_counter % frame_skip == 0:
            hand_landmarks = hand_detector.detect(img)
            HandController.hand_landmarks = hand_landmarks
            
            if hand_landmarks:
                HandController.update_fingers_status()
                HandController.cursor_moving()
                HandController.detect_zoomming()
                HandController.detect_clicking()
                HandController.detect_dragging()

        cv2.imshow('Hand Tracker', img)
        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
