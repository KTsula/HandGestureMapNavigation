import pyautogui

class HandController:
    prev_hand = None
    right_clicked = False
    left_clicked = False
    double_clicked = False
    dragging = False
    hand_landmarks = None
    pinky_down = None
    pinky_up = None
    index_down = None
    index_up = None
    middle_down = None
    middle_up = None
    ring_down = None
    ring_up = None
    thumb_down = None 
    thumb_up = None
    all_fingers_down = None
    all_fingers_up = None
    index_within_thumb = None
    middle_within_thumb = None
    pinky_within_thumb = None
    ring_within_thumb = None
    screen_width, screen_height = pyautogui.size()

    @staticmethod
    def update_fingers_status():
        HandController.pinky_down = HandController.hand_landmarks.landmark[20].y > HandController.hand_landmarks.landmark[17].y
        HandController.pinky_up = HandController.hand_landmarks.landmark[20].y < HandController.hand_landmarks.landmark[17].y
        HandController.index_down = HandController.hand_landmarks.landmark[8].y > HandController.hand_landmarks.landmark[5].y
        HandController.index_up = HandController.hand_landmarks.landmark[8].y < HandController.hand_landmarks.landmark[5].y
        HandController.middle_down = HandController.hand_landmarks.landmark[12].y > HandController.hand_landmarks.landmark[9].y
        HandController.middle_up = HandController.hand_landmarks.landmark[12].y < HandController.hand_landmarks.landmark[9].y
        HandController.ring_down = HandController.hand_landmarks.landmark[16].y > HandController.hand_landmarks.landmark[13].y
        HandController.ring_up = HandController.hand_landmarks.landmark[16].y < HandController.hand_landmarks.landmark[13].y
        HandController.thumb_down = HandController.hand_landmarks.landmark[4].y > HandController.hand_landmarks.landmark[13].y
        HandController.thumb_up = HandController.hand_landmarks.landmark[4].y < HandController.hand_landmarks.landmark[13].y

        HandController.all_fingers_down = (HandController.index_down and HandController.middle_down
                                       and HandController.ring_down and HandController.pinky_down)

        HandController.all_fingers_up = (HandController.index_up and HandController.middle_up
                                     and HandController.ring_up and HandController.pinky_up)

        HandController.index_within_thumb = (HandController.hand_landmarks.landmark[4].y <
                                                       HandController.hand_landmarks.landmark[8].y <
                                                       HandController.hand_landmarks.landmark[2].y)

        HandController.middle_within_thumb = (HandController.hand_landmarks.landmark[4].y <
                                                        HandController.hand_landmarks.landmark[12].y <
                                                        HandController.hand_landmarks.landmark[2].y)

        HandController.pinky_within_thumb = (HandController.hand_landmarks.landmark[4].y <
                                                        HandController.hand_landmarks.landmark[20].y <
                                                        HandController.hand_landmarks.landmark[2].y)

        HandController.ring_within_thumb = (HandController.hand_landmarks.landmark[4].y <
                                                      HandController.hand_landmarks.landmark[16].y <
                                                      HandController.hand_landmarks.landmark[2].y)

    @staticmethod
    def get_position(hand_x_position, hand_y_position):
        old_x, old_y = pyautogui.position()
        current_x = int(hand_x_position * HandController.screen_width)
        current_y = int(hand_y_position * HandController.screen_height)

        ratio = 1
        HandController.prev_hand = (current_x, current_y) if HandController.prev_hand is None else HandController.prev_hand
        delta_x = current_x - HandController.prev_hand[0]
        delta_y = current_y - HandController.prev_hand[1]
        
        HandController.prev_hand = [current_x, current_y]
        current_x , current_y = old_x + delta_x * ratio, old_y + delta_y * ratio

        threshold = 5
        if current_x < threshold:
            current_x = threshold
        elif current_x > HandController.screen_width - threshold:
            current_x = HandController.screen_width - threshold
        if current_y < threshold:
            current_y = threshold
        elif current_y > HandController.screen_height - threshold:
            current_y = HandController.screen_height - threshold

        return (current_x,current_y)
    
    @staticmethod
    def lerp(start, end, alpha):
        """Linear interpolation between start and end by alpha."""
        return start + (end - start) * alpha
        
    @staticmethod
    def cursor_moving():
        point = 9
        current_x, current_y = HandController.hand_landmarks.landmark[point].x, HandController.hand_landmarks.landmark[point].y
        x, y = HandController.get_position(current_x, current_y)
        
        # Check if previous hand position is set, otherwise initialize it
        if HandController.prev_hand is None:
            HandController.prev_hand = (x, y)
        
        # Determine the new cursor position with smoothing
        smooth_factor = 0.5  # Adjust this value to control the smoothing effect
        new_x = int(HandController.lerp(HandController.prev_hand[0], x, smooth_factor))
        new_y = int(HandController.lerp(HandController.prev_hand[1], y, smooth_factor))
        HandController.prev_hand = (new_x, new_y)
        
        cursor_freezed = HandController.all_fingers_up and HandController.thumb_down
        if not cursor_freezed:
            pyautogui.moveTo(new_x, new_y, duration=0)
            print("Cursor moving")  # Debug print statement

    @staticmethod
    def detect_zoomming():
        zoomming = (HandController.index_up and HandController.middle_up and HandController.ring_down
                    and HandController.pinky_down)
        window = .05
        index_touches_middle = (
                abs(HandController.hand_landmarks.landmark[8].x - HandController.hand_landmarks.landmark[12].x) <= window)
        zoomming_out = zoomming and index_touches_middle
        zoomming_in = zoomming and not index_touches_middle
        
        if zoomming_out:
            pyautogui.keyDown('ctrl')
            pyautogui.scroll(-50)
            pyautogui.keyUp('ctrl')
            print("Zooming Out")

        if zoomming_in:
            pyautogui.keyDown('ctrl')
            pyautogui.scroll(50)
            pyautogui.keyUp('ctrl')
            print("Zooming In")

    @staticmethod
    def detect_clicking():
        left_click_condition = (HandController.index_within_thumb and HandController.middle_up
                        and HandController.ring_up and HandController.pinky_up
                        and not HandController.middle_within_thumb
                        and not HandController.ring_within_thumb
                        and not HandController.pinky_within_thumb)
        if not HandController.left_clicked and left_click_condition:
            pyautogui.click()
            HandController.left_clicked = True
            print("Left Clicking")
        elif not HandController.index_within_thumb:
            HandController.left_clicked = False

        right_click_condition = (HandController.middle_within_thumb and HandController.index_up
                                 and HandController.ring_up and HandController.pinky_up
                                 and not HandController.index_within_thumb
                                 and not HandController.ring_within_thumb
                                 and not HandController.pinky_within_thumb)
        if not HandController.right_clicked and right_click_condition:
            pyautogui.rightClick()
            HandController.right_clicked = True
            print("Right Clicking")
        elif not HandController.middle_within_thumb:
            HandController.right_clicked = False

        double_click_condition = (HandController.ring_within_thumb and HandController.index_up
                                  and HandController.middle_up and HandController.pinky_up
                                  and not HandController.index_within_thumb
                                  and not HandController.middle_within_thumb
                                  and not HandController.pinky_within_thumb)
        if not HandController.double_clicked and double_click_condition:
            pyautogui.doubleClick()
            HandController.double_clicked = True
            print("Double Clicking")
        elif not HandController.ring_within_thumb:
            HandController.double_clicked = False
            
    @staticmethod
    def detect_dragging():
        if not HandController.dragging and HandController.all_fingers_down:
            pyautogui.mouseDown(button="left")
            HandController.dragging = True
            print("Dragging")
        elif not HandController.all_fingers_down:
            pyautogui.mouseUp(button="left")
            HandController.dragging = False
