import cv2

cv2.namedWindow('window')

capture = cv2.VideoCapture('./public/video.mp4')

FPS = capture.get(cv2.CAP_PROP_FPS)
width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
size = (width, height)

fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')

writer = cv2.VideoWriter(
    './public/video-out.avi',
    fourcc,
    FPS,
    (width, height)
)

while True:
    ret, frame = capture.read() 

    if not ret:
        break

    center = (width / 2, height / 2)

    logpolar_frame = cv2.warpPolar(
        frame,
        (width, height),
        center,
        40,
        cv2.INTER_LINEAR + cv2.WARP_POLAR_LOG
    )

    writer.write(logpolar_frame)

writer.release()
capture.release()
