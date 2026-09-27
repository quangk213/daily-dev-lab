import cv2 

res = [60, 56, 31]

img_path = './public/pic_3.jpg'

cv2.namedWindow("window2")
img = cv2.imread(img_path)
img_processed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('window', img_processed)

cv2.waitKey(0)
cv2.destroyAllWindows()


