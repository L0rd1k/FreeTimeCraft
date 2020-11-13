import DataSetMaker as dsm
import HeightEstimator as h_est
import FastDistortion as fd
import sys
import cv2
import os
import random
def main(argv):
    # cap = cv2.VideoCapture("/home/ilya/NetBeansProjects/os/build/OSRecordsPlayer/videos/video_2_2020-06-08 15:14:37.avi")
    # fast_d = fd.FastUndistort()
    #
    #
    # while (True):
    #     ret, frame = cap.read()
    #     distorted = fast_d.undistort("/home/ilya/intrinsics_down.yml", frame)
    #     cutImage = distorted[0:768, 150:918]
    #     image = cv.resize(cutImage, (248,248))
    #     if cv2.waitKey(30) & 0xFF == ord('q'):
    #         break
    #
    # cap.release()
    # cv2.destroyAllWindows()

    # fast_d = fd.FastUndistort()
    # src = fd.readImage("/home/ilya/569.jpg")
    # fast_d.undistort("/home/ilya/intrinsics_down.yml", src)
    # pth = "/home/ilya/PycharmProjects/Dataset/ImagesUndistort"
    # generalDataSet = [pth + '/{}'.format(i) for i in os.listdir(pth)]
    # print(generalDataSet)
    # random.shuffle(generalDataSet)
    # print("General DataSet: " + str(len(generalDataSet)))
    # fdr = fd.FastUndistort();
    # for itr, img_path in enumerate(generalDataSet):
    #     print(img_path)
    #     image = cv2.imread(img_path, cv2.IMREAD_COLOR)
    #     cutImage = image[0:768, 150:918]
    #     dist = cv2.resize(cutImage, (248, 248), interpolation= cv2.INTER_CUBIC)
    #     # dist = fdr.undistort("/home/ilya/intrinsics_down.yml", image)
    #     cv2.imwrite(str(generalDataSet[itr]), dist)

    he = h_est.HeightEstimator(1, 32)
    print("1 - Datset Generator\n2 - Train Dataset\n3 - Check GPU existance\n4 - Predict by image\n5 - Predict by video\n")
    global path
    path = "/opt/data/CNN/dataset_map2" if (len(argv) == 1) else argv[1]
    value = input("Input your value: ")
    if(value == '1'):
        print("Dataset generator\n")
        dsm.generateDesirableHeights(100, 10000, 50)
        mapImage = dsm.loadMap("/opt/data/Anna/sasmap18.jpg")
        dsm.getMapInfo(mapImage)
        dsm.cutMapImage(mapImage, "/opt/data/Anna/SAVE")
    elif(value == '2'):
        print("Dataset training\n")
        general_dataset = he.loadDataSet(path)
        images, labels = he.processDataSet(general_dataset, 248, 248)
        image_train, image_test, label_train, label_test = he.splitDataTrainAndTest(images, labels)
        model = he.buildModel()
        # model, history = he.trainModel(model, image_train, label_train)
        # he.showTrainingTable(history)
        model = he.loadWeights(model,"./weights_Main_2000/model_2000_val_mse179197.1094.hdf5")
        he.pedictHeight(model, image_test, label_test, image_train, label_train)
    elif(value == '3'):
        print("GPU output\n")
        he.gpuOutput()
    elif(value == '4'):
        model = he.buildModel()
        model = he.loadWeights(model,"./weights_Main_2000/model_1000_val_mse154801.5156.hdf5")
        he.predictByImageSet(model)
    elif (value == '5'):
        model = he.buildModel()
        model = he.loadWeights(model, "./weights_Main_2000/model_1000_val_mse154801.5156.hdf5")
        he.predictByVideo(model)

if __name__ == "__main__":
    main(sys.argv)

