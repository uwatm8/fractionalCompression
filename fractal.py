import numpy as np
import cv2
import sys
import time
import math

path = "./src.jpg"

height, width = cv2.imread(path, 0).shape
img = cv2.imread(path)


def getAreaAverage(x1, x2, y1, y2, img):
    return img[y1:y2, x1:x2].mean(axis=0).mean(axis=0)


def fillArea(x1, x2, y1, y2, img, value):
    height = len(img)
    width = len(img[0])
    for x in range(x2-x1):
        for y in range(y2-y1):
            if x+x1 < width and y+y1 < height:
                img[y+y1][x+x1] = value


def getAreaLoss(x1, x2, y1, y2, img):

    if True:

        avg = getAreaAverage(x1, x2, y1, y2, img)

        # fast method does not give same loss as slow version for some reason
        avgArr = [x[:] for x in [[avg] * (x2-x1)] * (y2-y1)]
        return abs(img[y1:y2, x1:x2] -
                   avgArr).sum(axis=0).sum(axis=0).sum(axis=0)
    else:
        loss = 0
        for x in range(x2-x1):
            for y in range(y2-y1):
                diff = abs(img[y][x]-avg)
                for i in range(len(diff)):
                    loss += diff[i]

        return loss


def getDeeperAreas(x1, x2, y1, y2, img, depth):

    xAvg = (x1+x2)//2
    yAvg = (y1+y2)//2

    return [{
        'x1': x1,
        'x2': xAvg,
        'y1': y1,
        'y2': yAvg,
        'loss': getAreaLoss(x1, xAvg, y1, yAvg, img),
        'depth': depth+1
    },
        {
        'x1': x1,
        'x2': xAvg,
        'y1': yAvg,
        'y2': y2,
        'loss': getAreaLoss(x1, xAvg, yAvg,  y2, img),
        'depth': depth+1
    },
        {
        'x1': xAvg,
        'x2': x2,
        'y1': y1,
        'y2': yAvg,
        'loss': getAreaLoss(xAvg, x2, y1, yAvg, img),
        'depth': depth+1
    },
        {
        'x1': xAvg,
        'x2': x2,
        'y1': yAvg,
        'y2': y2,
        'loss': getAreaLoss(xAvg, x2, yAvg, y2, img),
        'depth': depth+1
    },
    ]


avg = getAreaAverage(0, width, 0, height, img)
areas = []
areas = getDeeperAreas(0, width, 0, height, img, 1)
outImg = []

areas.sort(key=lambda x: x['loss'])


def printAreasLoss(areas):
    print("___")
    for i in range(len(areas)):
        print("loss", i, areas[i]['loss'])


for y in range(height):
    outImg.append([])
    for x in range(width):
        outImg[y].append([0, 0, 0])


def addToAreaQueue(area, areas):
    oldPivot = len(areas)
    pivot = len(areas) // 2
    areaLoss = area['loss']
    pivotChange = abs(math.ceil((pivot-oldPivot)))

    while oldPivot != pivot:
        oldPivot = pivot
        pivotLoss = areas[pivot]['loss']

        if areaLoss > pivotLoss:
            pivot += pivotChange
        else:
            pivot -= pivotChange

        pivot = max(0, min(len(areas)-1, pivot))
        pivotChange = abs(math.floor((pivot-oldPivot))//2)

    areas.insert(pivot, area)


def doAreaFractal(area, areas):
    areas.remove(area)

    areaAvg = getAreaAverage(area['x1'],
                             area['x2'], area['y1'], area['y2'], img)

    start2 = time.time()
    fillArea(area['x1'],
             area['x2'], area['y1'], area['y2'], outImg, areaAvg)
    end2 = time.time()
    start3 = time.time()
    newAreas = getDeeperAreas(area['x1'],
                              area['x2'], area['y1'], area['y2'], img, area['depth'])
    end3 = time.time()
    start4 = time.time()
    for newArea in newAreas:
        addToAreaQueue(newArea, areas)
    end4 = time.time()
    '''print('aaaaa')
    print('2', end2-start2)
    print('3', end3-start3)
    print('4', end4-start4)'''


maxDepth = 1000
maxFractalDepth = 0

for i in range(maxDepth):
    biggestLoss = 0
    biggestLossIndex = 3

    if not i % 20:
        print('i', i)

    biggestLossIndex = len(areas)-1

    doAreaFractal(areas[biggestLossIndex], areas)
    if maxFractalDepth < areas[biggestLossIndex]['depth']:
        maxFractalDepth = areas[biggestLossIndex]['depth']
        print('new max depth', maxFractalDepth)


npImg = np.uint8(outImg)
cv2.imwrite('frac.jpg', npImg)
