import cv2
import mediapipe as mp
import HandTrackingModule as htm
import time
import numpy as np

# Initialize variables for storing polygon coordinates
polygon_points = []
polygon_created = False

screen_width, screen_height = 640, 480
cap = cv2.VideoCapture(1)
cap.set(3, screen_width)
cap.set(4, screen_height)

detector = htm.handDetector(detectionCon=0.5)

pTime = 0
cTime = 0


def create_polygon(event, x, y, flags, param):
    global polygon_points, polygon_created

    if event == cv2.EVENT_LBUTTONDOWN:
        polygon_points.append((x, y))
        polygon_created = True

    elif event == cv2.EVENT_RBUTTONDOWN:
        polygon_points = []
        polygon_created = False

    elif event == cv2.EVENT_LBUTTONDBLCLK:
        polygon_created = True


cv2.namedWindow('Hand Detection')
cv2.setMouseCallback('Hand Detection', create_polygon)

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)

    if len(lmlist) > 0:
        wrist_x = lmlist[0][1]
        wrist_y = lmlist[0][2]

        if polygon_created:
            if cv2.pointPolygonTest(np.array(polygon_points), (wrist_x, wrist_y), False) >= 0:
                position_text = "Inside"
            else:
                position_text = "Outside"
        else:
            position_text = "Polygon not created"

        cv2.putText(img, position_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    for i in range(len(polygon_points)):
        cv2.line(img, polygon_points[i], polygon_points[(i + 1) % len(polygon_points)], (0, 255, 0), 2)

    for point in polygon_points:
        cv2.circle(img, point, 5, (255, 0, 0), -1)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.imshow('Hand Detection', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
