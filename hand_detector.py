import mediapipe as mp
import cv2

class HandDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.75, 
            min_tracking_confidence=0.75
        )
        self.mp_draw = mp.solutions.drawing_utils

    def detect(self, image):
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            self.mp_draw.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
            return hand_landmarks
        return None