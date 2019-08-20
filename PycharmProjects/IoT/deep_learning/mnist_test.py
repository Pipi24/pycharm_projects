#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-3-8 下午7:23
# @Author  : Wuhiu
# @Email   : wuhiugo@163.com
# @File    : baseAnalyzer.py
# @Software: PyCharm

# from tensorflow.examples.tutorials.mnist import input_data
#
# mnist = input_data.read_data_sets('/home/wuhiu/deeplearning', one_hot=True)
#
# print("training data size:", mnist.train.num_examples)
# print(mnist.train.images[0])
# from array import *
# data = array('B')
# print(data)
# data.append(0)
# print(data)
# a={'a':1, 'b':0, 'c':1, 'd':0}
# print(type(a))
# for key in list(a.keys()):
#     print(a)
#     print(type(a))
#     del a[key]
#     print(a)
#     print(type(a))

import numpy as np

a = np.array([], dtype='float32')
b = np.array([1.0, 2.0, 3.0], dtype='float32')
a = np.concatenate((a, b))
print(a)
print(b[-1:])
