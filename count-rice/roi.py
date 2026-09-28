import cv2
import numpy as np

cv2.namedWindow('window')
img = cv2.imread('./public/img_1.jpg')

h, w, c = img.shape
print(h)
print(w)

roi = img[70:150, 200:350, :]
cv2.imshow('roi', roi)

roi[:,:,:] = 255

cv2.imshow('window', img)
cv2.waitKey(0)
cv2.destroyAllWindows()