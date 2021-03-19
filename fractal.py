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


def getAreaAverage(x1, x2, y1, y2, img):
    acc = [0, 0, 0]
    for x in range(x2-x1):
        for y in range(y2-y1):
            acc += img[y+y1][x+x1]

    return acc // ((x2-x1)*(y2-y1))


def fillArea(x1, x2, y1, y2, img, value):
    height = len(img)
    width = len(img[0])
    for x in range(x2-x1):
        for y in range(y2-y1):
            if x+x1 < width and y+y1 < height:
                img[y+y1][x+x1] = value
            else:
                print('yo', x+x1, y+y1)


def getAreaLoss(x1, x2, y1, y2, img):
    avg = getAreaAverage(x1, x2, y1, y2, img)
    loss = 0
    for x in range(x2-x1):
        for y in range(y2-y1):
            diff = abs(img[y][x]-avg)
            for i in range(len(diff)):
                loss += diff[i]
    return loss


rowAvg = []
columnAvg = []

avg = getAreaAverage(0, width-1, 0, height-1, img)

areas = []


def getDeeperAreas(x1, x2, y1, y2, img):

    xAvg = (x1+x2)//2
    yAvg = (y1+y2)//2

    return [{
        'x1': x1,
        'x2': xAvg,
        'y1': y1,
        'y2': yAvg
    },
        {
        'x1': x1,
        'x2': xAvg,
        'y1': yAvg,
        'y2': y2-1
    },
        {
        'x1': xAvg,
        'x2': x2-1,
        'y1': y1,
        'y2': yAvg
    },
        {
        'x1': xAvg,
        'x2': x2-1,
        'y1': yAvg,
        'y2': y2-1
    },
    ]


areas = getDeeperAreas(0, width, 0, height, img)


outImg = []
for y in range(height):
    outImg.append([])
    for x in range(width):
        outImg[y].append(avg)

for area in areas:
    areaLoss = getAreaLoss(area['x1'],
                           area['x2'], area['y1'], area['y2'], img)
    print('area', area)
    print('loss', areaLoss)

    areaAvg = getAreaAverage(area['x1'],
                             area['x2'], area['y1'], area['y2'], img)

    fillArea(area['x1'],
             area['x2'], area['y1'], area['y2'], outImg, areaAvg)

npImg = np.uint8(outImg)
cv2.imwrite('frac.jpg', npImg)
