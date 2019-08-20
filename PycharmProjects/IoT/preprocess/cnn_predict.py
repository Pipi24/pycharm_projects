#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @DATE    : 19-4-23
# @Time    : 下午8:34
# @Author  : wuhiu
# @Email   : wuhiugo@163.com
# @File    : cnn_predict
# @Software: PyCharm

import numpy as np
from keras.models import load_model

MODEL_DIR = '/home/wuhiu/deeplearning/5_Model/classify_traffic_nonvpn.h5'


def predict(x_pred):
    x_pred = np.array(x_pred)
    x_pred = np.expand_dims(x_pred, axis=2)
    model = load_model(MODEL_DIR)
    preds = model.predict_classes(x_pred)
    preds = preds.tolist()
    return preds
