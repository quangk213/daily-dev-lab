import cv2

cv2.namedWindow('window')
capture = cv2.VideoCapture('./public/video.mp4')

while True:
    ret, frame = capture.read()
    if not ret:
        break
    cv2.imshow('window', frame) 
    key = cv2.waitKey(33) 
    if key == 27:
        break

capture.release()
cv2.destroyAllWindows()