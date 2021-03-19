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


def fillArea(x1, x2, y1, y2, img, value):
    for x in range(x2-x1):
        for y in range(y2-y1):
            img[x+x1][y+y1] = value


diff = []
for y in range(height):
    yStepSize = height // buckets

    diff.append([])
    avg = img[y:y+1].mean(axis=0).mean(axis=0)
    for x in range(width):
        xStepSize = width // buckets

        pixel1 = img[y:y+1, x:x+1][0][0]

        if False:
            print(xStepSize)
            print(yStepSize)

        avg = pixel1
        print("diff", diff)
        print("avg", avg)

        fillArea(x, x+1, y, y+1, img, avg)

        diff[y].append(avg)

npImg = np.uint8(diff)
# cv2.imshow("image", np.uint8(diff))
cv2.imwrite('out.jpg', npImg)
