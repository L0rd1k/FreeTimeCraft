import cv2 as cv
import numpy as np
import os

class DatasetGenerator:
    rectSize = list()
    heightsList = []
    numberOfImages = list()
    cutImageList = list()

    def __init__(self, minHeight, maxHeight, step, map):
        self.__minHeight = minHeight
        self.__maxHeight = maxHeight
        self.__step = step
        self.__mapPath = map
        self.__generateUsableHeights()

    def __generateUsableHeights(self):
        print("... height generation in process ...")
        for itr, elem in enumerate(range(self.__minHeight, self.__maxHeight + 1, self.__step)):
            self.heightsList.append(int(elem))
        self.__getMapInfo(self.__loadMap())

    def __loadMap(self):
        print("... map loading ... ")
        original_map = cv.imread(self.__mapPath)
        return original_map

    def __getMapInfo(self, mapImage):
        print("... map data processing ... ")

        widthMap = float(input('Width of map in meters: ')) # 14010
        widthFrame = 4056 * 0.00000155
        focalLength = 0.005
        distance = widthMap * focalLength / widthFrame
        print("------\nWidthMap: " + str(widthMap) + "\nWidthFrame: " + str(focalLength) + "\nDistance: " + str(
            distance) + "\n------")
        for height in self.heightsList:
            dim = min((height * np.size(mapImage, 0) // distance),
                      (3040 * (height * np.size(mapImage, 0) // distance) // 4056))
            self.rectSize.append(int(dim))

        self.__cutMapImage(mapImage)

    def __cutMapImage(self, mapImage):
        print("... cutting map for dataset ... ")
        height, width, channels = mapImage.shape
        os.mkdir("./Dataset")
        for itr, curDimensions in enumerate(self.rectSize):
            self.numberOfImages.append((height // self.rectSize[itr]) * (width // self.rectSize[itr]))
            if (itr == 0):
                self.__slicingOperation(mapImage, "./Dataset", itr, height, width, curDimensions)
            elif ((itr != 0) and (self.numberOfImages[itr - 1] > self.numberOfImages[itr])):
                self.__slicingOperation(mapImage, "./Dataset", itr, height, width, curDimensions)

        print("All images saved!!!" + str(sum(self.numberOfImages)))

    def __slicingOperation(self, mapImage, datasetFolderPath, itr, height, width, curDimensions):
        print("-> Number of images to generate: " + str(self.numberOfImages[itr]))
        for i in range(height // self.rectSize[itr]):
            for j in range(width // self.rectSize[itr]):
                cutImage = mapImage[i * self.rectSize[itr]: i * self.rectSize[itr] + self.rectSize[itr],
                           j * self.rectSize[itr]: j * self.rectSize[itr] + self.rectSize[itr]]
                path = datasetFolderPath + "/Image_H" + str(self.heightsList[itr]) + "_D" + str(
                    curDimensions - 1) + "_R" + str(i) + "C" + str(j) + ".jpg"
                cv.imwrite(path, cutImage)
