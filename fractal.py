import numpy as np
import cv2
import sys
import time
import math

debug = True

path = "./src.jpg"

height, width = cv2.imread(path, 0).shape
img = cv2.imread(path)


def getAreaAverage(x1, x2, y1, y2, img):
    if x2-x1 == 0 or y2-x1 == 0:
        print('getting area average of empty slice')
        return [0, 0, 0]

    arrSlice = img[y1:y2, x1:x2]

    if not len(arrSlice):
        return [0, 0, 0]

    return arrSlice.mean(axis=0).mean(axis=0)


def fillArea(x1, x2, y1, y2, img, value):
    '''npImg = np.array(img)
    npImg[y1:y2, x1:x2] = [x[:] for x in [[value] * (x2-x1)] * (y2-y1)]
    img = npImg.tolist()'''

    height = len(img)
    width = len(img[0])
    for x in range(x2-x1):
        for y in range(y2-y1):
            if x+x1 < width and y+y1 < height:
                img[y+y1][x+x1] = value


def getAreaLoss(x1, x2, y1, y2, img):

    if x2-x1 == 0 or y2-x1 == 0:
        return 0

    avg = getAreaAverage(x1, x2, y1, y2, img)

    if True or (y2-y1 > 2 and y2-y1 > 2):
        # fast method does not give same loss as slow version for some reason
        avgArr = [x[:] for x in [[avg] * (x2-x1)] * (y2-y1)]

        if not len(avgArr):
            return 0

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

    fillArea(area['x1'], area['x2'], area['y1'], area['y2'], outImg, areaAvg)

    newAreas = getDeeperAreas(area['x1'],
                              area['x2'], area['y1'], area['y2'], img, area['depth'])
    for newArea in newAreas:
        addToAreaQueue(newArea, areas)


maxDepth = 50000
maxFractalDepth = 0

biggestLossIndex = 0
for i in range(maxDepth):
    biggestLoss = 0

    biggestLossIndex = len(areas)-1

    doAreaFractal(areas[biggestLossIndex], areas)
    if debug and not i % 1000:
        if i != 0:
            print('i', i)

    if maxFractalDepth < areas[biggestLossIndex]['depth']:
        maxFractalDepth = areas[biggestLossIndex]['depth']
        print('new max depth', maxFractalDepth)

print('estimated size: ', ((maxDepth*3 + maxDepth*maxFractalDepth)/4000), 'kb')

npImg = np.uint8(outImg)
cv2.imwrite('out/frac.jpg', npImg)
