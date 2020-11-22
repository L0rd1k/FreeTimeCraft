from imutils import paths
import ImageProcessing.GammaCorection as gmc
import argparse
import matplotlib.pyplot as plt
import cv2
import os

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


# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--images", required=True, help="path to input directory of images")
# ap.add_argument("-t", "--threshold", type=float, default=100.0, help="focus measures that fall below this value will be considered 'blurry'")
# args = vars(ap.parse_args())
#
# mat_list = list()
# focus_measure_list = list()
# gamma_measure_list = list()
# counterPlus = 0
# counter = 0
#
# img_list = list(paths.list_images(args["images"]))
# img_list.sort(key=os.path.getmtime)
# for itr, imagePath in enumerate(img_list):
#     image = cv2.imread(imagePath)
#
#     # APPLY BLURRING TO DATASET
#     blur_value = BlurDetector.getBluring(image)
#
#     # APPLY GAMMA TO DATASET
#     gamma_image = gmc.adjust_gamma(image, gamma=0.75)
#     cv2.imwrite("D:/FullDataSet/Gamma/image_{}.jpg".format(itr), gamma_image)
#     # fm_gamma = BlurDetector.getBluring(gamma_image)
#
#     print("{} - {} - {}".format(itr, imagePath, blur_value))
#     text = "Not Blurry"
#     focus_measure_list.append(blur_value)
#     #gamma_measure_list.append(fm_gamma)
#     if blur_value < args["threshold"]:
#         focus_measure_list.append(blur_value)
#         mat_list.append(image)
#         counterPlus += 1
#         text = "Blurry"
#     counter += 1
#
# print("Min {} / Max {}".format(min(focus_measure_list), max(focus_measure_list)))
# print("{} / {}".format(counter, counterPlus))
# percentage = (counterPlus * 100) / counter
#
#
# def show_image():
#     for elem in mat_list:
#         cv2.putText(image, "{}: {:.2f}".format(text, blur_value), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
#         cv2.imshow("Image", image)
#         key = cv2.waitKey(0)
#     cv2.destroyAllWindows()
#
#
#
# def draw_graphic():
#     fig = plt.figure(figsize=(10, 5))
#     plt.scatter(range(len(focus_measure_list)), focus_measure_list, s=3, edgecolors='none', c='green')
#     plt.scatter(range(len(gamma_measure_list)), gamma_measure_list, s=3, edgecolors='none', c='orange')
#     plt.plot([0, len(focus_measure_list)], [args["threshold"], args["threshold"]],  color='red', linestyle='dashed', marker='o', markerfacecolor='blue', markersize=1)
#     ax = fig.add_subplot(111)
#     ax.set_xlabel('Images [I]')
#     ax.set_ylabel('Quality [Q]')
#     ax.text(0.9, 1, "Amount: {} / Below threshold: {} \n Percentage1: {} %".format(counter, counterPlus, format(percentage,'.2f')),
#             horizontalalignment='right', verticalalignment='top', transform=ax.transAxes)
#     plt.legend()
#     plt.show()
#
# draw_graphic()
