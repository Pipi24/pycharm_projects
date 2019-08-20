#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-3-8 下午7:23
# @Author  : Wuhiu
# @Email   : wuhiugo@163.com
# @File    : baseAnalyzer.py
# @Software: PyCharm
import os
import errno
from array import *
import numpy
from PIL import Image
import binascii
import numpy as np

import pandas as pd
import matplotlib.pyplot as plt
import binascii

from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv1D, MaxPool1D
from keras.optimizers import SGD
from keras.utils.vis_utils import plot_model

BATCH_SIZE = 50
SEQ_LEN = 784
LEARNING_RATE = 1e-4
EPOCHS = 40
NUM_CLASSES = 6
NUM_CHANNELS = 1


def get_data():
    with open('/home/wuhiu/deeplearning/data/data', 'rb') as f:
        data = f.read()
    print(data)
    print(type(data))
    print(len(data))
    data = binascii.hexlify(data)
    data = np.array([int(data[i:i+2], 16) for i in range(0, len(data), 2)])
    data = np.reshape(data, (-1, 784, 1))
    print(data)
    print(len(data))
    x_train = data.astype('float32')
    x_train /= 255
    y_train = to_categorical(np.random.randint(NUM_CLASSES, size=(len(data), 1)), num_classes=NUM_CLASSES)
    print(y_train)
    return x_train, y_train


def show_train_history(history):
    plt.plot(history.history['loss'])
    plt.plot(history.history['acc'])
    # plt.plot(history.history['val_loss'])
    # plt.plot(history.history['val_acc'])
    plt.title('Train History')
    plt.ylabel('Acc')
    plt.xlabel('Epoch')
    plt.legend(['loss', 'acc'], loc='upper left')
    plt.show()


def cnn_model(x_train, y_train):
    model = Sequential()
    model.add(Conv1D(filters=32, kernel_size=25, strides=1, padding='same', activation='relu', input_shape=(SEQ_LEN, NUM_CHANNELS)))
    model.add(MaxPool1D(pool_size=3, strides=3, padding='same'))
    model.add(Conv1D(filters=64, kernel_size=25, strides=1, padding='same', activation='relu'))
    model.add(MaxPool1D(pool_size=3, strides=3, padding='same'))
    model.add(Flatten())
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(NUM_CLASSES, activation='softmax'))
    sgd = SGD(lr=LEARNING_RATE, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    history = model.fit(x_train, y_train, batch_size=BATCH_SIZE, epochs=EPOCHS)
    # score = model.evaluate(x_test, y_test, batch_size=32)
    print(model.summary())
    plot_model(model, to_file='/home/wuhiu/model.png', show_shapes=True)
    show_train_history(history)


if __name__ == '__main__':
    x_train, y_train = get_data()
    cnn_model(x_train, y_train)








# hex_session = binascii.hexlify(data)
#         # print(hexst)
# byte_session = np.array([int(hex_session[i:i+2], 16) for i in range(0, len(hex_session), 2)])
# print(len(byte_session))

# data_image = array('B')
# print(data_image)
#
# print("3:",os.path.join('aaaa','./bbb','ccccc.txt'))
# PNG_SIZE = 28
#
# def getMatrixfrom_pcap(filename,width):
#     with open(filename, 'rb') as f:
#         content = f.read()
#     hexst = binascii.hexlify(content)
#     fh = numpy.array([int(hexst[i:i+2],16) for i in range(0, len(hexst), 2)])
#     rn = len(fh)/width
#     fh = numpy.reshape(fh[:rn*width],(-1,width))
#     fh = numpy.uint8(fh)
#     return fh
# def mkdir_p(path):
#     try:
#         os.makedirs(path)
#     except OSError as exc:  # Python >2.5
#         if exc.errno == errno.EEXIST and os.path.isdir(path):
#             pass
#         else:
#             raise
#
# paths = [['3_ProcessedSession\TrimedSession\Train', '4_Png\Train'],['3_ProcessedSession\TrimedSession\Test', '4_Png\Test']]
# for p in paths:
#     for i, d in enumerate(os.listdir(p[0])):
#         dir_full = os.path.join(p[1], str(i))
#         mkdir_p(dir_full)
#         for f in os.listdir(os.path.join(p[0], d)):
#             bin_full = os.path.join(p[0], d, f)
#             im = Image.fromarray(getMatrixfrom_pcap(bin_full,PNG_SIZE))
#             png_full = os.path.join(dir_full, os.path.splitext(f)[0]+'.png')
#             im.save(png_full)