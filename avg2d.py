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


rowAvg = []
columnAvg = []

outImg = []
for y in range(height):
    rowAvg.append(img[y:y+1].mean(axis=0).mean(axis=0))

for x in range(width):
    # TODO optimize
    acc = [0, 0, 0]
    for y in range(height):
        acc += img[y, x]

    columnAvg.append(acc / height)

# row avg
'''for y in range(height):
    outImg.append([])
    for x in range(width):
        outImg[y].append(rowAvg[y])'''

# column avg
for y in range(height):
    outImg.append([])
    for x in range(width):
        outImg[y].append((rowAvg[y]+columnAvg[x])/2)

npImg = np.uint8(outImg)
cv2.imwrite('avg2d.jpg', npImg)
