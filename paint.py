import numpy as np
import cv2
from collections import deque

# Detects red color
lower_red = np.array([161, 155, 84])
upper_red = np.array([179, 255, 255])

bpoints = [deque(maxlen=512)]
gpoints = [deque(maxlen=512)]
rpoints = [deque(maxlen=512)]
ypoints = [deque(maxlen=512)]
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
cv2.putText(paintWindow, "RED", (298, 33),
    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2,
    cv2.LINE_AA)
cv2.putText(paintWindow, "YELLOW", (520, 33),
    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2,
    cv2.LINE_AA)

cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

# Capturing video
camera = cv2.VideoCapture(cv2.CAP_V4L2)

while True:
    (grabbed, frame) = camera.read()
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    if not grabbed:
        break