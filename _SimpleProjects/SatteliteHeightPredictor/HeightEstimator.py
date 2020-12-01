import numpy as np
import matplotlib.pyplot as plt
from keras import callbacks
from sklearn.model_selection import train_test_split
from tensorflow.python.client import device_lib
import cv2 as cv
import os, re, random, gc

from Utils.performance import timer
import CNNModels.sattelite_regression_model as cnnmodel
import Utils.easystring as es
import ImageProcessing.BlurDetector as blur
import ImageProcessing.GammaCorection as gamma
import ImageProcessing.FastDistortion as fast_d

class HeightEstimator:
    images = list()
    labels = list()
    blur_list = list()
    wrong_img = 0
    max_height_label = 0
    def __init__(self, epoch, b_size):
        self.epoch = epoch
        self.batch_size = b_size
        self.mainLoop()

    def mainLoop(self):
        # default_path = "D:/FullDataSet/Combined"
        # dataset_list = self.loadDataSet(default_path)
        # images, labels = self.processDataSet(dataset_list, 248, 248)
        # image_train, image_test, label_train, label_test = self.splitDataTrainAndTest(images, labels)
        model = cnnmodel.sattelite_12_layer_regression_model()
        # model, history = self.trainModel(model, image_train, label_train)
        # self.showTrainingTable(history)
        # self.predictHeight(model, image_test, label_test, image_train, label_train)

        self.loadWeights(model, "D:\GitProjects\FreeTimeCraft\_SimpleProjects\SatteliteHeightPredictor\weights\model_0200_val_mse0.0014.hdf5")
        self.predictByVideo(model)

    @timer
    def loadDataSet(self, datasetPath):
        generalDataSet = [datasetPath + '/{}'.format(i) for i in os.listdir(datasetPath)]
        random.shuffle(generalDataSet)
        print("Input DataSet Size: " + str(len(generalDataSet)))
        gc.collect()
        return generalDataSet

    def rotate_image(self, image):
        angle_list = [90, 180, -90, -180]
        random_angle = random.choice(angle_list)
        rotated_image = cv.flip(image, random_angle)
        return rotated_image

    @timer
    def processDataSet(self, list_of_images, nrows, ncols):
        for itr, img_path in enumerate(list_of_images):
            image_values = list()
            [image_values.append(int(float(s))) for s in re.findall(r'-?\d+\.?\d*', es.split_path(img_path))]
            if int(image_values[0]) <= 1000:
                orig_image = cv.imread(img_path, cv.IMREAD_COLOR)

                for gamma_value in np.arange(0.5, 2.0, 0.25):
                    adjusted = gamma.adjust_gamma(orig_image, gamma=gamma_value)
                    blur_value_gamma = blur.BlurDetector.getBluring(adjusted)
                    if blur_value_gamma > 50:
                        if gamma_value != 1.0:
                            adjusted = self.rotate_image(adjusted)
                        self.images.append(cv.resize(adjusted, (nrows, ncols), interpolation=cv.INTER_CUBIC))
                        self.labels.append(int(image_values[0]))
                        self.blur_list.append(blur_value_gamma)
                    else:
                        self.wrong_img += 1

        print("DataSet Size after augmentation: {}".format(len(self.images)))
        print("Wrong image size: {}".format(self.wrong_img))

        value = sorted(zip(self.labels, self.blur_list))
        height_val = list(map(lambda x: x[0], value))
        blur_val = list(map(lambda x: x[1], value))

        fig, axs = plt.subplots(2)
        axs[0].scatter(range(len(self.images)), blur_val, s=3, edgecolors='none', c='blue')
        axs[1].scatter(range(len(self.images)), height_val, s=3, edgecolors='none', c='green')

        for step_value in range(0,len(self.images), int(len(self.images)*1/5)):
            axs[1].plot([step_value, step_value],
                        [0, 1000],
                        color='red', linestyle='dashed',
                        marker='o', markerfacecolor='blue', markersize=1)
        plt.show()
        return self.images, self.labels

    @timer
    def splitDataTrainAndTest(self, images, labels):
        image_train, image_test, label_train, label_test = train_test_split(np.array(images), np.array(labels), test_size=0.20, random_state=2)
        self.max_height_label = label_train.max()
        image_train = image_train.astype('float32') / 255.0
        image_test = image_test.astype('float32') / 255.0
        label_train = label_train.astype('float32') / label_train.max()
        label_test = label_test.astype('float32') / label_train.max()
        return image_train, image_test, label_train, label_test

    @timer
    def trainModel(self, model, image_train, label_train):
        filepath = "./weights/model_{epoch:04d}_val_mse{val_mean_squared_error:.4f}.hdf5"
        checkpoint = callbacks.ModelCheckpoint(filepath, monitor='loss', verbose=1,
                                               save_best_only=False, mode='auto', period=50)
        history = model.fit(image_train, label_train, batch_size=self.batch_size, epochs=self.epoch,
                            shuffle=True, verbose=1, validation_split=0.2, callbacks=[checkpoint])
        model.save_weights('./weights/final_model_height_data.hdf5')
        return model, history

    @timer
    def showTrainingTable(self, history):
        epochs = range(1, len(history.history['mean_squared_error']) + 1)
        fig, axs = plt.subplots(2)
        axs[0].plot(epochs, history.history['mean_squared_error'], 'b', label='Training accuracy')
        axs[0].plot(epochs, history.history['val_mean_squared_error'], 'r', label='Validation accuracy')
        axs[0].set(title='Training and Validation accuracy',
               ylabel='Value')
        axs[1].plot(epochs, history.history['loss'], 'g', label='Training loss')
        axs[1].plot(epochs, history.history['val_loss'], 'y', label='Validation loss')
        axs[1].set(title='Training and Validation loss',
               ylabel='Value')
        plt.show()

    @timer
    def predictHeight(self, model, image_test, label_test, image_train, label_train):
        test_value = model.evaluate(image_test, label_test, verbose=0)

        print('Test loss: {} / Test accuracy: {}'.format(test_value[0], test_value[1]))
        predicted_height = model.predict(image_test, batch_size=1)

        value = sorted(zip(label_test, predicted_height * self.max_height_label))
        lbl_val = list(map(lambda x: x[0], value))
        pred_val = list(map(lambda x: x[1], value))

        fig, axs = plt.subplots(2)
        axs[0].scatter(range(len(lbl_val)), pred_val, s=3, edgecolors='none', c='blue')
        axs[0].scatter(range(len(lbl_val)), lbl_val, s=3, edgecolors='none', c='red')
        plt.show()

        for itr, elem in enumerate(image_test):
            print("{} - {}".format(lbl_val[itr], pred_val[itr]))

    @timer
    def loadWeights(self, model, path):
        model.load_weights(path)
        return model

    @timer
    def predictByImageSet(self, model):
        list_images = self.loadDataSet("./images2")
        images = list()
        labels = list()
        fast_d = fd.FastUndistort()
        for itr, img_path in enumerate(list_images):
            frame = cv.imread(img_path, cv.IMREAD_COLOR)
            distorted = fast_d.undistort("/home/ilya/intrinsics_down.yml", frame)
            cutImage = cv.resize(distorted[0:768, 150:918], (248, 248))
            image_values = list()
            [image_values.append(int(float(s))) for s in re.findall(r'-?\d+\.?\d*', self.pathLeaf(img_path))]
            labels.append(int(image_values[0]))
            images.append(cutImage)

        np_image = np.array(images)
        newValue = model.predict(np_image, batch_size=1)
        for itr, elem in enumerate(np_image):
            print(str(labels[itr]) + " - " + str(newValue[itr]))


    def predictByVideo(self, model):
        cap = cv.VideoCapture("D:/FullDataSet/videos/test_video_2.avi")

        dist_obj = fast_d.FastUndistort()
        predict_list = list()

        # out = cv.VideoWriter("./videos/record.avi", cv.VideoWriter_fourcc('M', 'J', 'P', 'G'), 25, (248, 248))
        # realHeight = list()
        # with open("./videos/video_height_data_2020-06-09 17:15:49.txt") as inputfile:
        #     for line in inputfile:
        #         realHeight.append(line)

        iterator_video_frame = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            distorted = dist_obj.undistort("D:\GitProjects\FreeTimeCraft\_SimpleProjects\SatteliteHeightPredictor\ConfigsData\intrinsics_down.yml", frame)
            cutImage = distorted[0:768,0:768]
            image = cv.resize(cutImage, (248, 248))
            images = list()
            images.append(image)
            np_image = np.array(images)
            predictedValue = model.predict(np_image, batch_size=1)
            iterator_video_frame += 1
            predict_list.append(float(predictedValue * 1000))

        cap.release()
        cv.destroyAllWindows()
        plt.plot(predict_list, 'o', markersize=2, linewidth=1, color='green')
        plt.xlabel('Frame (hr)')
        plt.ylabel('Height (km)')
        plt.show()

            # cutImage = distorted[0:768, 150:918]
            # image = cv.resize(cutImage, (248, 248))
            # images = list()
            # images.append(image)
            # np_image = np.array(images)
            # newValue = model.predict(np_image, batch_size=1)
            # print(str(realHeight[itr]) + " / " + str(newValue))
            # image = cv.putText(image, str(newValue), (20,20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv.LINE_AA)
            # image = cv.putText(image, str(realHeight[itr]), (20,40), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv.LINE_AA)

            #out.write(image)
            # cv.imshow("Image", image)
            # itr+=1
            # if cv.waitKey(1) & 0xFF == ord('q'):
            #     break

        # cap.release()
        # out.release()
        # cv.destroyAllWindows()


    # def checkRangeValue(self, moduleInc):
    #     return moduleInc




    # def loadVideoFile(self, path, gz):
    #     img = cv.imread(path, cv.IMREAD_COLOR)


