#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-3-8 下午7:23
# @Author  : Wuhiu
# @Email   : wuhiugo@163.com
# @File    : baseAnalyzer.py
# @Software: PyCharm
import os
import binascii
import numpy as np
from keras.utils import to_categorical

NUM_CLASSES = 6
x_train = np.array([], dtype='float32')
y_train = []
dict_6class_novpn = {'non-vpn_Chat': 0, 'non-vpn_Email': 1, 'non-vpn_File Transfer': 2, 'non-vpn_P2P': 3, 'non-vpn_Streaming': 4, 'non-vpn_VoIP': 5}


def get_pcaps_path(dataset_root_dir_path):
    dirs_name = os.listdir(dataset_root_dir_path)
    # print(dirs_name)
    data_path = []
    label_path = []
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
                    data_path.append(pcap_path)
                if '_label' in pcap_name:
                    pcap_path = os.path.join(class_dir_path, pcap_name)
                    print(pcap_path)
                    label_path.append(pcap_path)
    # print(pcaps_path)
    data_path.sort()
    label_path.sort()
    print(data_path)
    print(label_path)
    print('data_path len is: ', len(data_path))
    print('label_path len is: ', len(label_path))
    return data_path, label_path


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

    # with open('/home/wuhiu/deeplearning/PreprocessData/data_train', 'w') as f:
    #     f.write(x_train)
    # y_train = to_categorical(np.random.randint(NUM_CLASSES, size=(len(data), 1)), num_classes=NUM_CLASSES)
    # print(y_train)
    # return x_train, y_train


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




if __name__ == '__main__':
    DIR_PATH = '/home/wuhiu/deeplearning/VPNData'
    data_paths, label_paths = get_pcaps_path(DIR_PATH)
    # get_data(data_paths)
    get_label(label_paths)
    # y_t = to_categorical(np.random.randint(NUM_CLASSES, size=(2052, 1)), num_classes=NUM_CLASSES)

