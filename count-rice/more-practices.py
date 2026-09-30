import cv2
import numpy as np
import math

img = cv2.imread('./public/img_1.jpg')

b, g, r = cv2.split(img)

print(g)

clone1 = img.copy()
clone1[:, :, 0] = 0
clone1[:, :, 2] = 0

min, max, minLoc, maxLoc = cv2.minMaxLoc(g)

print(min, max, minLoc, maxLoc)

thresh = int((max - min) / 2)

clone1[:, :, 1] = thresh

clone2 = cv2.compare(img, clone1, cv2.CMP_GT)

c2g = clone2[:, :, 1]
print(c2g)

print(cv2.minMaxLoc(c2g))

cv2.imshow('clone1', clone1)

cv2.imshow('window', img)

cv2.waitKey(0)
cv2.destroyAllWindows()