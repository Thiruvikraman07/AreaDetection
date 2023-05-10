import cv2
import mediapipe as mp
import HandTrackingModule as htm

# Initialize variables for storing line coordinates
line_start = None
line_end = None
line_created = False

screen_width, screen_height = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, screen_width)
cap.set(4, screen_height)

detector = htm.handDetector(detectionCon=0.5)

def create_line(event, x, y, flags, param):
    global line_start, line_end, line_created

    if event == cv2.EVENT_LBUTTONDOWN:
        line_start = (x, y)
        line_end = None
        line_created = False

    elif event == cv2.EVENT_LBUTTONUP:
        line_end = (x, y)
        line_created = True


cv2.namedWindow('Hand Detection')
cv2.setMouseCallback('Hand Detection', create_line)

while True:

    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)


    for point in lmlist:

        x = point[1]
        y = point[2]
        if line_created:
            if x < min(line_start[0], line_end[0]):
                position_text = "Left"
            elif x > max(line_start[0], line_end[0]):
                position_text = "Right"
            elif y < min(line_start[1], line_end[1]):
                position_text = "Above"
            elif y > max(line_start[1], line_end[1]):
                position_text = "Below"
            else:
                position_text = "On Line"
        else:
            position_text = "Line not created"

        cv2.putText(img, position_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,cv2.LINE_AA)

    if line_start is not None:
        cv2.circle(img, line_start, 5, (255, 0, 0), -1)
        if line_end is not None:
            cv2.line(img, line_start, line_end, (0, 0, 255), 2)


    cv2.imshow('Hand Detection', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
