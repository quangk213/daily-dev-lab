import cv2

cv2.namedWindow('Image-in')
cv2.namedWindow('Image-out')

img = cv2.imread('./public/img_1.jpg')
img_out = cv2.GaussianBlur(img, (3, 3), 0)

cv2.imshow('Image-in', img)
cv2.imshow('Image-out', img_out)

cv2.waitKey(0)
cv2.destroyAllWindows()