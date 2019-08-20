#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @DATE    : 19-4-23
# @Time    : 下午8:57
# @Author  : wuhiu
# @Email   : wuhiugo@163.com
# @File    : predict
# @Software: PyCharm

MODEL_DIR = '/home/wuhiu/deeplearning/5_Model/classify_traffic_nonvpn.h5'
import binascii
import os

import numpy
import numpy as np
from keras.models import load_model

PNG_SIZE = 28
UNIFY_DIR = '/home/wuhiu/deeplearning/2_UnifySession/'
IMAGE_DIR = '/home/wuhiu/deeplearning/3_SessionImage/'


def get_one_dim_form(filename):
    with open(filename, 'rb') as f:
        content = f.read()
    hexst = binascii.hexlify(content)
    fh = numpy.array([int(hexst[i:i + 2], 16) for i in range(0, len(hexst), 2)])
    fh = fh.astype('float32')
    fh /= 255
    return fh


def get_cnn_input():
    input_data = []
    for i, d in enumerate(os.listdir(UNIFY_DIR)):
        files = os.listdir(os.path.join(UNIFY_DIR, d))
        files.sort()
        print(files)
        for f in files:
            bin_full = os.path.join(UNIFY_DIR, d, f)
            input_data.append(get_one_dim_form(bin_full))
    # print('input data: ', input_data)
    return input_data


x = get_cnn_input()
# x = np.array(x)
# x = np.expand_dims(x, axis=2)
# model = load_model(MODEL_DIR)
# preds = model.predict_classes(x)
# preds = preds.tolist()
# print(preds)
# print(type(preds))
