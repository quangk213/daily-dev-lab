import cv2
import numpy as np
import time

cv2.namedWindow('window')

img = cv2.imread('./public/img_1.jpg')

def mouse_callback(event, x, y, flags, param, radius=20):
    if event == cv2.EVENT_LBUTTONDOWN:
       if radius == 50:
            return
       cv2.circle(param, (x, y), radius=radius, color=(0, 255, 0), thickness=5) 

cv2.setMouseCallback('window', mouse_callback, img)

while True:
    dump = img.copy()
    cv2.imshow('ori', img)

    cv2.imshow('window', dump)

    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()
