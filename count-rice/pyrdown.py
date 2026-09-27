import cv2

cv2.namedWindow('img-in')
cv2.namedWindow('img-out')

img = cv2.imread('./public/img_1.jpg')
img_pyr = cv2.pyrDown(img)

cv2.imshow('img-in', img)
cv2.imshow('img-out', img_pyr)

cv2.waitKey(0)
cv2.destroyAllWindows()