import cv2
import numpy as np
import math

img = np.zeros((210, 210), dtype=np.uint8)

h, w = img.shape

for i in range(0, 210, 20):
    offset = i // 2
    roi = img[offset : (h - offset), offset : (w - offset)] 
    roi[:] = i

cv2.imshow('window', img)

cv2.waitKey(0)
cv2.destroyAllWindows()