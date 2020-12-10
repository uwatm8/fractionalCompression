import numpy as np
import cv2
import sys
print(sys.version)

path = "./src.jpg"

height, width = cv2.imread(path, 0).shape
img = cv2.imread(path)

print(height)
print(width)

buckets = 2

average = img.mean(axis=0).mean(axis=0)

print(average)

diff = []
for i in range(height):
    diff.append([])
    avg = img[i:i+1].mean(axis=0).mean(axis=0)
    for j in range(width):
        pixel1 = img[i, j]

        r = pixel1[0]
        g = pixel1[1]
        b = pixel1[2]

        diff[i].append(avg)

npImg = np.uint8(diff)
# cv2.imshow("image", np.uint8(diff))
cv2.imwrite('out.jpg', npImg)
