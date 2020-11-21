import numpy as np
import matplotlib.pyplot as plt
from keras import layers, models, callbacks
from sklearn.model_selection import train_test_split
from tensorflow.python.client import device_lib
import cv2 as cv
import ntpath
import os
import re
import random
import gc

import FastDistortion as fd
import Utils.UsefulTools as ut

class HeightEstimator:
    def __init__(self, epoch, b_size):
        self.epoch = epoch
        self.batch_size = b_size
        self.mainLoop()

    def mainLoop(self):
        default_path = "./Dataset"
        dataset_list = self.loadDataSet(default_path)
        images, labels = self.processDataSet(dataset_list, 512, 512)
        self.splitDataTrainAndTest(images, labels)

    def gpuOuput(self):
        print(device_lib.list_local_devices())

    def pathLeaf(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)


    @ut.timer
    def loadDataSet(self, datasetPath):
        generalDataSet = [datasetPath + '/{}'.format(i) for i in os.listdir(datasetPath)]
        random.shuffle(generalDataSet)
        print("General DataSet: " + str(len(generalDataSet)))
        gc.collect()
        return generalDataSet


    @ut.timer
    def processDataSet(self, list_of_images, nrows, ncols):
        images = list()
        labels = list()
        for itr, img_path in enumerate(list_of_images):
            image_values = list()
            images.append(cv.resize(cv.imread(img_path, cv.IMREAD_COLOR), (nrows, ncols), interpolation=cv.INTER_CUBIC))
            [image_values.append(int(float(s))) for s in re.findall(r'-?\d+\.?\d*', self.pathLeaf(img_path))]
            labels.append(int(image_values[0]))
        return images, labels


    @ut.timer
    def splitDataTrainAndTest(self, images, labels):
        np_images = np.array(images)
        np_labels = np.array(labels)

        # image_train, image_test, label_train, label_test = train_test_split(np_images, np_labels, test_size=0.20, random_state=2)
        # print("Shape of image_train:", image_train.shape)
        # print("Shape of image_test:", image_test.shape)
        # print("Shape of label_train:", label_train.shape)
        # print("Shape of label_test:", label_test.shape)
        # image_train = image_train.astype('float32')
        # image_test = image_test.astype('float32')
        # label_train = label_train.astype('float32')
        # label_test = label_test.astype('float32')
        # image_train /= 255
        # image_test /= 255
        # label_train /= 10000
        # label_test /= 10000
        # return image_train, image_test, label_train, label_test

    def buildModel(self):
        model = models.Sequential()
        model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(248, 248, 3)))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(128, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(128, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Flatten())
        model.add(layers.Dropout(0.5))
        model.add(layers.Dense(512, activation='relu'))
        model.add(layers.Dense(1))
        model.summary()
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mean_squared_error'])
        # model.save("./models/model_12_layer")
        return model

    def trainModel(self, model, image_train, label_train):
        filepath = "./weights3/model_{epoch:04d}_val_mse{val_mean_squared_error:.4f}.hdf5"
        checkpoint = callbacks.ModelCheckpoint(filepath, monitor='loss', verbose=1,
                                               save_best_only=False, mode='auto', period=10)
        history = model.fit(image_train, label_train, batch_size=self.batch_size, epochs=self.epoch,
                            shuffle=True, verbose=1, validation_split=0.2, callbacks=[checkpoint])
        model.save_weights('./weights3/final_model_height_data.h5')
        return model, history

    def showTrainingTable(self, history):
        epochs = range(1, len(history.history['mean_squared_error']) + 1)
        plt.plot(epochs, history.history['mean_squared_error'], 'b', label='Training accuracy')
        plt.plot(epochs, history.history['val_mean_squared_error'], 'r', label='Validation accuracy')
        plt.title('Training and Validation accuracy')
        plt.legend()
        plt.figure()
        plt.plot(epochs, history.history['loss'], 'b', label='Training loss')
        plt.plot(epochs, history.history['val_loss'], 'r', label='Validation loss')
        plt.title('Training and Validation loss')
        plt.legend()
        plt.show()

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
        cap = cv.VideoCapture("/home/ilya/NetBeansProjects/os/build/OSRecordsPlayer/videos/video_2_2020-06-09 16:33:50.avi")
        fast_d = fd.FastUndistort()
        out = cv.VideoWriter("./videos/record.avi", cv.VideoWriter_fourcc('M', 'J', 'P', 'G'), 25, (248, 248))
        realHeight = list()
        with open("./videos/video_height_data_2020-06-09 17:15:49.txt") as inputfile:
            for line in inputfile:
                realHeight.append(line)
        itr = 0
        while (True):
            ret, frame = cap.read()
            distorted = fast_d.undistort("/home/ilya/intrinsics_down.yml", frame)
            cutImage = distorted[0:768, 150:918]
            image = cv.resize(cutImage, (248, 248))
            images = list()
            images.append(image)
            np_image = np.array(images)
            newValue = model.predict(np_image, batch_size=1)
            print(str(realHeight[itr]) + " / " + str(newValue))
            image = cv.putText(image, str(newValue), (20,20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv.LINE_AA)
            # image = cv.putText(image, str(realHeight[itr]), (20,40), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv.LINE_AA)

            #out.write(image)
            cv.imshow("Image", image)
            itr+=1
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        out.release()
        cv.destroyAllWindows()


    def checkRangeValue(self, moduleInc):
        return moduleInc

    def pedictHeight(self, model, image_test, label_test, image_train, label_train):
        score = model.evaluate(image_test, label_test, verbose=0)
        print('Test loss:', score[0])
        print('Test accuracy:', score[1])
        imgs_ts = image_test[0:50]
        newValue = model.predict(imgs_ts, batch_size=1)
        for itr, elem in enumerate(imgs_ts):
            print(str(label_test[itr]) + str(newValue[itr]))

    def loadWeights(self, model, path):
        model.load_weights(path)
        return model

    def loadVideoFile(self, path, gz):
        img = cv.imread(path, cv.IMREAD_COLOR)


