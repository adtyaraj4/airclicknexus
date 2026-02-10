import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time



# Initialize Mediapipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Capture video from webcam
cap = cv2.VideoCapture(0)

# Get screen width and height for mouse control
screen_width, screen_height = pyautogui.size()

# Thresholds for gestures
click_threshold = 45  # Increased for easier click gesture
volume_threshold = 40  # Reduced for more sensitive volume control

# Initialize previous volume
current_volume = 50  # Starting volume (0 to 100)
pyautogui.press('volumemute')  # Mute to start
time.sleep(0.1)  # Give time to apply mute

# Smoothing parameters for mouse movement
smoothing_factor = 0.1  # Reduced for more responsive mouse movement
prev_mouse_x, prev_mouse_y = pyautogui.position()

# Volume control cooldown (shortened)
volume_cooldown = 0.1  # Shortened cooldown for volume adjustments
last_volume_change_time = time.time()

# Screenshot cooldown
screenshot_taken = False
last_screenshot_time = time.time()

# Click hold duration
click_hold_duration = 0.2  # Seconds to hold for click
last_click_time = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Flip the image horizontally
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Process the image and detect hand landmarks
    result = hands.process(img_rgb)
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Get landmarks for fingers
            index_finger_tip = hand_landmarks.landmark[8]
            thumb_tip = hand_landmarks.landmark[4]
            middle_finger_tip = hand_landmarks.landmark[12]  # Get middle finger tip
            pinky_tip = hand_landmarks.landmark[20]

            # Convert normalized hand coordinates to screen coordinates
            finger_x = int(index_finger_tip.x * screen_width)
            finger_y = int(index_finger_tip.y * screen_height)
            thumb_x = int(thumb_tip.x * screen_width)
            thumb_y = int(thumb_tip.y * screen_height)
            middle_x = int(middle_finger_tip.x * screen_width)
            middle_y = int(middle_finger_tip.y * screen_height)
            pinky_x = int(pinky_tip.x * screen_width)
            pinky_y = int(pinky_tip.y * screen_height)

            # Smooth mouse movement
            new_mouse_x = int(prev_mouse_x * (1 - smoothing_factor) + finger_x * smoothing_factor)
            new_mouse_y = int(prev_mouse_y * (1 - smoothing_factor) + finger_y * smoothing_factor)
            pyautogui.moveTo(new_mouse_x, new_mouse_y)
            prev_mouse_x, prev_mouse_y = new_mouse_x, new_mouse_y

            # Calculate distances for gesture recognition
            distance_thumb_index = np.linalg.norm(np.array([finger_x, finger_y]) - np.array([thumb_x, thumb_y]))
            distance_index_middle = np.linalg.norm(np.array([finger_x, finger_y]) - np.array([middle_x, middle_y]))

            # Handle click gesture (using index and thumb)
            if distance_thumb_index < click_threshold:
                current_time = time.time()
                if current_time - last_click_time > click_hold_duration:
                    pyautogui.click()  # Perform a mouse click
                    cv2.putText(img, "Click!", (finger_x, finger_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    last_click_time = current_time  # Reset last click time for the next click

            # Handle volume control gestures
            current_time = time.time()
            if current_time - last_volume_change_time > volume_cooldown:
                if distance_index_middle > volume_threshold and current_volume < 100:
                    current_volume += 1  # Increase volume gradually
                    pyautogui.press('volumeup')
                    last_volume_change_time = current_time
                    cv2.putText(img, f"Volume Up! ({current_volume})", (finger_x, finger_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                elif distance_index_middle < volume_threshold and current_volume > 0:
                    current_volume -= 1  # Decrease volume gradually
                    pyautogui.press('volumedown')
                    last_volume_change_time = current_time
                    cv2.putText(img, f"Volume Down! ({current_volume})", (finger_x, finger_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Keyboard control gestures
            if distance_thumb_index < click_threshold and distance_index_middle < click_threshold:
                pyautogui.press('esc')
                cv2.putText(img, "Escape!", (finger_x, finger_y + 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Raise hand for "Up Arrow"
            if finger_y < screen_height / 3:
                pyautogui.press('up')
                cv2.putText(img, "Up Arrow!", (finger_x, finger_y + 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Lower hand for "Down Arrow"
            elif finger_y > (screen_height * 2 / 3):
                pyautogui.press('down')
                cv2.putText(img, "Down Arrow!", (finger_x, finger_y + 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Check for "Thumbs Up" gesture to take a screenshot
            thumb_cmc = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            thumb_up_condition = thumb_tip.y < thumb_cmc.y  # Thumb is raised
            index_finger_extended = index_tip.y < thumb_cmc.y  # Index is extended

            if thumb_up_condition and index_finger_extended:
                if time.time() - last_screenshot_time > 2:  # Screenshot cooldown
                    if not screenshot_taken:
                        screenshot = pyautogui.screenshot()
                        timestamp = time.strftime("%Y%m%d_%H%M%S")  # Timestamp for filename
                        screenshot.save(f'screenshot_{timestamp}.png')
                        print("Screenshot taken!")
                        screenshot_taken = True
                        last_screenshot_time = time.time()  # Update the last screenshot time
            else:
                screenshot_taken = False  # Reset flag if gesture is no longer detected

            # Draw hand landmarks on the image
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Highlight finger tips
            cv2.circle(img, (finger_x, finger_y), 10, (255, 0, 0), -1)  # Index finger tip
            cv2.circle(img, (thumb_x, thumb_y), 10, (255, 0, 0), -1)  # Thumb tip
            cv2.circle(img, (middle_x, middle_y), 10, (255, 0, 0), -1)  # Middle finger tip
            cv2.circle(img, (pinky_x, pinky_y), 10, (255, 0, 0), -1)  # Pinky tip

    # Display the video feed
    cv2.imshow("Hand Gesture Mouse Control", img)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
