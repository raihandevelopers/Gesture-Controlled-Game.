from tkinter import Frame
import cv2 as cv
import mediapipe as mp
from pynput.keyboard import Key, Controller

keyboard = Controller()

mp_draw = mp.solutions.drawing_utils 
mp_hand = mp.solutions.hands

fingerTipIds = [4, 8, 12, 16, 20]

video = cv.VideoCapture(0)

hands = mp_hand.Hands(min_detection_confidence = 0.5, min_tracking_confidence = 0.5)

while True:
    success, image = video.read()

    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

    image.flags.writeable = False
    results = hands.process(image)
    image.flags.writeable = True

    image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

    landmarks_list = []

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[-1]

        for index, lm in enumerate(hand_landmarks.landmark):
            h, w, c = image.shape # Height, Width, Channels
            cx, cy = int(lm.x*w), int(lm.y*h)
            landmarks_list.append([index, cx, cy])

        mp_draw.draw_landmarks(image, hand_landmarks, mp_hand.HAND_CONNECTIONS)

    fingers_open = []

    if len(landmarks_list) != 0:
        for tipId in fingerTipIds:
            if tipId == 4:
                if landmarks_list[tipId][1] > landmarks_list[tipId - 1][1]:
                    fingers_open.append(1)
                else: 
                    fingers_open.append(0)
            else:
                if landmarks_list[tipId][2] < landmarks_list[tipId - 2][2]:
                    fingers_open.append(1)
                else: 
                    fingers_open.append(0)

    count_fingers_open = fingers_open.count(1)

    if results.multi_hand_landmarks != None:

        if count_fingers_open == 0:
            cv.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv.FILLED)
            cv.putText(image, "BRAKE", (45, 375), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)

            keyboard.press(Key.left)
            keyboard.release(Key.right)

        elif count_fingers_open == 5:
            cv.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv.FILLED)
            cv.putText(image, "GAS", (45,  375), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)

            keyboard.press(Key.right)
            keyboard.release(Key.left)

    else:
        keyboard.release(Key.right)
        keyboard.release(Key.left)


    cv.imshow("Frame", image)
    
    # Closing the Program if q is Pressed.
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv.destroyAllWindows()

#CODE BY - RAIHAN KHAN.