from imutils import paths
import argparse
import cv2

__author__ = "Ilya Petrikov"


class BlurDetector:
    def __init__(self):
        pass

    @classmethod
    def __variance_of_laplacian(cls, bgr_image):
        grayscale_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        return cv2.Laplacian(grayscale_image, cv2.CV_64F).var()

    @classmethod
    def getBluring(cls, bgr_image):
        return cls.__variance_of_laplacian(bgr_image)


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True, help="path to input directory of images")
ap.add_argument("-t", "--threshold", type=float, default=100.0, help="focus measures that fall below this value will be considered 'blurry'")
args = vars(ap.parse_args())

for imagePath in paths.list_images(args["images"]):
    print(imagePath)
    image = cv2.imread(imagePath)
    fm = BlurDetector.getBluring(image)
    text = "Not Blurry"
    if fm < args["threshold"]:
        text = "Blurry"
    cv2.putText(image, "{}: {:.2f}".format(text, fm), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
    cv2.imshow("Image", image)
    key = cv2.waitKey(0)

cv2.destroyAllWindows()