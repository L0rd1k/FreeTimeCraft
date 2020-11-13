import cv2
import numpy as np

class CalibrationData:
    #def __init__(self):
    camera_intrinsics = list()
    camera_distortion = list()
    image_size = (0, 0)
    calibration_error = 0.0

def loadCalib(filename):
    fs = cv2.FileStorage(filename, cv2.FILE_STORAGE_READ)
    camera_intrinsics = fs.getNode("m")
    camera_distortion = fs.getNode("d")


def readImage(imagepath):
    image = cv2.imread(imagepath, cv2.IMREAD_COLOR)
    cv2.imshow("Original Image", image)
    return image


class FastUndistort:
    def undistort(self, filename, src):
        fs = cv2.FileStorage(filename, cv2.FILE_STORAGE_READ)
        camera_intrinsics = fs.getNode("m")
        camera_distortion = fs.getNode("d")
        w, h = src.shape[0], src.shape[1]
        # gray = (np.float32(self._cameraMatrix), cv2.IMREAD_COLOR)
        mapx, mapy = cv2.initUndistortRectifyMap(np.float32(camera_intrinsics.mat()),
                                                 np.float32(camera_distortion.mat()),
                                                 None,
                                                 np.float32(camera_intrinsics.mat()),
                                                 (h, w),
                                                 5)
        dst = cv2.remap(src, mapx, mapy, cv2.INTER_LINEAR)
        return dst

