from turtle import color
import numpy as np
import cv2
from collections import deque

# Detects red color
lower_red = np.array([161, 155, 84])
upper_red = np.array([179, 255, 255])

bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]
bindex, gindex, rindex, yindex = 0, 0, 0, 0

colors = [(255,0,0), (0,255,0), (0,0,255), (0,255,255)]

color_index = 0

# Create a window
paintWindow = np.zeros((471, 636, 3)) + 255
paintWindow = cv2.rectangle(paintWindow, (40,1), (140,65), (0,0,0), 2)
paintWindow = cv2.rectangle(paintWindow, (160,1), (255,65), colors[0], -1)
paintWindow = cv2.rectangle(paintWindow, (275,1), (370,65), colors[1], -1)
paintWindow = cv2.rectangle(paintWindow, (390,1), (485,65), colors[2], -1)
paintWindow = cv2.rectangle(paintWindow, (505,1), (600,65), colors[3], -1)

cv2.putText(paintWindow, "CLEAR ALL", (49, 33),
    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2,
    cv2.LINE_AA)
cv2.putText(paintWindow, "BLUE", (185, 33),
    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2,
    cv2.LINE_AA)
cv2.putText(paintWindow, "GREEN", (298, 33),
    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2,
    cv2.LINE_AA)
cv2.putText(paintWindow, "RED", (420, 33),
    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2,
    cv2.LINE_AA)
cv2.putText(paintWindow, "YELLOW", (520, 33),
    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2,
    cv2.LINE_AA)

cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

# Capturing video
camera = cv2.VideoCapture(0)

while True:
    (grabbed, frame) = camera.read()
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    if not grabbed:
        break

    frame = cv2.rectangle(frame, (40,1), (140,65), (122,122,122), -1)
    frame = cv2.rectangle(frame, (160,1), (255,65), colors[0], -1)
    frame = cv2.rectangle(frame, (275,1), (370,65), colors[1], -1)
    frame = cv2.rectangle(frame, (390,1), (485,65), colors[2], -1)
    frame = cv2.rectangle(frame, (505,1), (600,65), colors[3], -1)
    cv2.putText(frame, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)

    # Preprocess input
    kernel = np.ones((5,5), np.uint8)
    Mask = cv2.inRange(hsv, lower_red, upper_red)
    Mask = cv2.erode(Mask, kernel, iterations=2)
    Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, kernel)
    Mask = cv2.dilate(Mask, kernel, iterations=1)

    (cnts, _) = cv2.findContours(Mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    center = None

    if len(cnts) > 0:
        cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
        ((x,y), radius) = cv2.minEnclosingCircle(cnt)
        cv2.circle(frame, (int(x), int(y)), int(radius), (0,255,255), 2)
        M = cv2.moments(cnt)
        center = (int(M['m10']/M['m00']), int(M['m01'] / M['m00']))

        if center[1] <= 65:
            if 40 <= center[0] <= 140:
                bpoints = [deque(maxlen=512)]
                gpoints = [deque(maxlen=512)]
                rpoints = [deque(maxlen=512)]
                ypoints = [deque(maxlen=512)]
                bindex, gindex, rindex, yindex = 0, 0, 0, 0
                paintWindow[67:,:,:] = 255
            elif 160 <= center[0] <= 255:
                color_index = 0
            elif 275 <= center[0] <= 370:
                color_index = 1
            elif 390 <= center[0] <= 485:
                color_index = 2
            elif 505 <= center[0] <= 600:
                color_index = 3
        else:
            if color_index == 0:
                bpoints[bindex].appendleft(center)
            elif color_index == 1:
                gpoints[gindex].appendleft(center)
            elif color_index == 2:
                rpoints[rindex].appendleft(center)
            elif color_index == 3:
                ypoints[yindex].appendleft(center)
    else:
        bpoints.append(deque(maxlen=512))
        bindex += 1
        gpoints.append(deque(maxlen=512))
        gindex += 1
        rpoints.append(deque(maxlen=512))
        rindex += 1
        ypoints.append(deque(maxlen=512))
        yindex += 1

    points = [bpoints, gpoints, rpoints, ypoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k-1] is None or points[i][j][k] is None:
                    continue
                cv2.line(frame, points[i][j][k-1], points[i][j][k], colors[i], 2)
                cv2.line(paintWindow, points[i][j][k-1], points[i][j][k], colors[i], 2)

    # Display output
    cv2.imshow("Web_cam_video", frame)
    cv2.imshow("Paint", paintWindow)
    cv2.imshow("Mask", Mask)

    if cv2.waitKey(1) & 0xFF ==ord("q"):
        break

camera.release()
cv2.destroyAllWindows()