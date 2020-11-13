import cv2 as cv
import numpy as np

rectSize = list()
heightsList = []
numberOfImages = list()
cutImageList = list()

def generateDesirableHeights(minHeight, maxHeight, step):
    for itr, elem in enumerate(range(minHeight, maxHeight+1, step)):
        heightsList.append(int(elem))


def loadMap(mapPath):
    originalMap = cv.imread(mapPath)
    return originalMap

def getMapInfo(mapImage):
    widthMap = float(input('Width of map in meters: '))
    widthFrame = 4056 * 0.00000155
    focalLength = 0.005
    distance = widthMap * focalLength / widthFrame
    print("------\nWidthMap: " + str(widthMap) + "\nWidthFrame: "+ str(focalLength) + "\nDistance: " + str(distance)+"\n------")
    for height in heightsList:
        dim = min((height * np.size(mapImage, 0) // distance),
                  (3040 * (height * np.size(mapImage, 0) // distance) // 4056))
        rectSize.append(int(dim))
        # print("Height: " + str(height) + " / RectSize: " + str(dim) + " x " + str(dim))

def cutMapImage(mapImage, datasetFolderPath):
    height, width, channels = mapImage.shape
    for itr, curDimensions in enumerate(rectSize):
        numberOfImages.append((height // rectSize[itr]) * (width // rectSize[itr]))
        if(itr == 0):
            slicingOperation(mapImage, datasetFolderPath, itr, height, width, curDimensions)
        elif((itr != 0) and (numberOfImages[itr-1] > numberOfImages[itr])):
            slicingOperation(mapImage, datasetFolderPath, itr, height, width, curDimensions)
    print("All images saved!!!" + str(sum(numberOfImages)))

def slicingOperation(mapImage, datasetFolderPath, itr, height, width, curDimensions):
    print("Number of images to generate: " + str(numberOfImages[itr]))
    for i in range(height // rectSize[itr]):
        for j in range(width // rectSize[itr]):
            cutImage = mapImage[i * rectSize[itr]: i * rectSize[itr] + rectSize[itr],
                                j * rectSize[itr]: j * rectSize[itr] + rectSize[itr]]
            path = datasetFolderPath + "/Image_H" + str(heightsList[itr]) + "_D" + str(curDimensions - 1) + "_R" + str(i) + "C" + str(j) + ".jpg"
            # cv.imwrite(path, cutImage)