import cv2
import numpy as np

cv2.namedWindow('window')

img = cv2.imread('./public/img_1.jpg')

h, w, c = img.shape

blend = np.zeros((h, w, 3), dtype=np.uint8)
blend[:,:,:] = 70

dst = cv2.addWeighted(img, 0.7, blend, 0.5, 0)

cv2.imshow('dst', dst)

cv2.imshow('blend', blend)

cv2.imshow('window', img)
cv2.waitKey(0)
cv2.destroyAllWindows()