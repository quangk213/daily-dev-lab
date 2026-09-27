import cv2
import pytesseract
import image_processor as imp

img = cv2.imread('public/invoice-test.png')
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_gray = imp.get_grayscale(img)
# img_gray = imp.remove_noise(img_gray)
# img_gray = imp.thresholding(img_gray)
# img_gray = imp.dilate(img_gray)

h, w, c = img.shape

# print(pytesseract.image_to_string(img_gray, lang='vie'))

# boxes = pytesseract.image_to_boxes(img_gray )

# for b in boxes.splitlines():
#     b = b.split(' ')
#     img = cv2.rectangle(img_gray, ((int(b[1])), h - (int(b[2]))), ((int(b[3])), h - (int(b[4]))), (0, 255, 0))

d = pytesseract.image_to_data(img_gray, output_type=pytesseract.Output.DICT)

n_boxes = len(d['text'])
for i in range(n_boxes):
    if int(d['conf'][i]) > 60:
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        img_gray  = cv2.rectangle(img_gray, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow('window', img_gray)

cv2.waitKey(0)
cv2.destroyAllWindows()

