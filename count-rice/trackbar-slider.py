import cv2

cv2.namedWindow('window')

g_slide_pos = 0
capture = cv2.VideoCapture('./public/video.mp4')

def onTrackbarSlide(pos):
    capture.set(cv2.CAP_PROP_POS_FRAMES, pos)    


frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

cv2.createTrackbar(
    'Position',
    'window',
    g_slide_pos,
    frames,
    onTrackbarSlide
)

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
