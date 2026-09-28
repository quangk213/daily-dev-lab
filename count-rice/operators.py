import cv2
import numpy as np

a = np.uint8([
    [1, 2],
    [3, 4]
])

b = np.uint8([
    [5, 6],
    [7, 253]
])

res = cv2.add(a, b)
print(res)

np_res = a + b
print(np_res)

