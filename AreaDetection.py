import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
screen_width, screen_height = 640, 480


cap = cv2.VideoCapture(1)
cap.set(3, screen_width)
cap.set(4, screen_height)

detector = htm.handDetector(detectionCon=0.5)
pTime=0
cTime=0

while True:

    success,img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img,draw=False)

    if len(lmlist)!=0:

        hand_center_x = int(lmlist[0][1])
        print(hand_center_x)
        middle_line_x = int(screen_width / 2)

        cv2.line(img, (middle_line_x, 0), (middle_line_x, screen_height), (255, 0, 0), 2)

        if hand_center_x < middle_line_x:
            side_text = "Left"
        else:
            side_text = "Right"

        cv2.putText(img, side_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break