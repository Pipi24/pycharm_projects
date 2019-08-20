#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-3-8 下午7:23
# @Author  : Wuhiu
# @Email   : wuhiugo@163.com
# @File    : baseAnalyzer.py
# @Software: PyCharm

#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-3-8 下午7:23
# @Author  : Wuhiu
# @Email   : wuhiugo@163.com
# @File    : baseAnalyzer.py
# @Software: PyCharm
# from keras.backend.tensorflow_backend import set_session
# import tensorflow as tf
# from keras import backend as K
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import binascii
import os

from keras import regularizers
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv1D, MaxPool1D
from keras.optimizers import SGD, Adam
from keras.utils.vis_utils import plot_model
from keras.callbacks import EarlyStopping

BATCH_SIZE = 16
SEQ_LEN = 784
LEARNING_RATE = 1e-4
EPOCHS = 60
NUM_CLASSES = 6
NUM_CHANNELS = 1


dict_6class_novpn = {'non-vpn_Chat': 0, 'non-vpn_Email': 1, 'non-vpn_File Transfer': 2, 'non-vpn_P2P': 3, 'non-vpn_Streaming': 4, 'non-vpn_VoIP': 5}
# config = tf.ConfigProto()
# config.gpu_options.allow_growth = True
# set_session(tf.Session(config=config))
x_train = np.array([])
y_train = []

def show_train_history(history):
    plt.plot(history.history['loss'][5:40])
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_loss'])
    plt.plot(history.history['val_acc'])
    plt.title('Train History')
    plt.ylabel('Acc')
    plt.xlabel('Epoch')
    plt.legend(['loss', 'acc', 'val_loss', 'val_acc'], loc='upper left')
    plt.show()


def get_pcaps_path(dataset_root_dir_path):
    dirs_name = os.listdir(dataset_root_dir_path)
    # print(dirs_name)
    data_paths = []
    label_paths = []
    for dir_name in dirs_name:
        # print(dir_name)
        dir_path = os.path.join(dataset_root_dir_path, dir_name)
        # print(dir_path)
        class_dirs_name = os.listdir(dir_path)
        # print(class_dirs_name)
        for class_dir_name in class_dirs_name:
            class_dir_path = os.path.join(dir_path, class_dir_name)
            # print(class_dir_path)
            pcaps_name = os.listdir(class_dir_path)
            for pcap_name in pcaps_name:
                # print(pcap_name)
                if '_data' in pcap_name:
                    pcap_path = os.path.join(class_dir_path, pcap_name)
                    print(pcap_path)
                    data_paths.append(pcap_path)
                if '_label' in pcap_name:
                    pcap_path = os.path.join(class_dir_path, pcap_name)
                    print(pcap_path)
                    label_paths.append(pcap_path)
    # print(pcaps_path)
    data_paths.sort()
    label_paths.sort()
    print(data_paths)
    print(label_paths)
    print('data_path len is: ', len(data_paths))
    print('label_path len is: ', len(label_paths))
    return data_paths, label_paths


def get_data(data_paths):
    global x_train
    for data_path in data_paths:
        with open(data_path, 'rb') as f:
            data = f.read()
        print(data)
        print(type(data))
        print(len(data))
        data = binascii.hexlify(data)
        data = np.array([int(data[i:i + 2], 16) for i in range(0, len(data), 2)])
        x_train = np.concatenate((x_train, data))
        # x_train.append(data)

    print(x_train)
    print(len(x_train))


def get_label(label_paths):
    global y_train
    for label_path in label_paths:
        with open(label_path, 'r') as f:
            label = f.read()
        label_split = label.split(',')
        label_split = label_split[0:-1]
        # print(label_split)
        for key in label_split:
            y_train.append(dict_6class_novpn[key])

    print(y_train)
    print((len(y_train)))
    y_train = to_categorical(y_train, num_classes=NUM_CLASSES)
    print(y_train)
    print((len(y_train)))

def cnn_model():
    global x_train
    x_train = np.reshape(x_train, (-1, 784, 1))
    x_train = x_train.astype('float32')
    x_train /= 255
    model = Sequential()
    model.add(Conv1D(filters=32, kernel_size=25, strides=1, padding='same', activation='relu', input_shape=(SEQ_LEN, NUM_CHANNELS)))
    # model.add(Dropout(0.5))
    model.add(MaxPool1D(pool_size=3, strides=3, padding='same'))
    model.add(Conv1D(filters=64, kernel_size=25, strides=1, padding='same', activation='relu'))
    # model.add(Dropout(0.5))
    model.add(MaxPool1D(pool_size=3, strides=3, padding='same'))
    model.add(Flatten())
    model.add(Dense(1024))
    model.add(Dropout(0.5))
    model.add(Dense(NUM_CLASSES, activation='softmax'))
    sgd = SGD(lr=LEARNING_RATE, decay=1e-5, momentum=0.9, nesterov=True, )
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, verbose=2, mode='auto')
    history = model.fit(x_train, y_train, validation_split=0.1, batch_size=BATCH_SIZE, epochs=EPOCHS, callbacks=[early_stopping])
    # score = model.evaluate(x_test, y_test, batch_size=32)
    print(model.summary())
    plot_model(model, to_file='/home/wuhiu/model.png', show_shapes=True)
    show_train_history(history)
    # K.clear_session()
    # tf.reset_default_graph()


if __name__ == '__main__':
    DIR_PATH = '/home/wuhiu/deeplearning/VPNData'
    data_paths, label_paths = get_pcaps_path(DIR_PATH)
    get_data(data_paths)
    get_label(label_paths)
    cnn_model()



