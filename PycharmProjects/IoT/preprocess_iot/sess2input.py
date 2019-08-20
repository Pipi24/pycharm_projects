#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-3-8 下午7:23
# @Author  : Wuhiu
# @Email   : wuhiugo@163.com
# @File    : baseAnalyzer.py
# @Software: PyCharm

import binascii
import errno
import os

import numpy
from PIL import Image

PNG_SIZE = 28
UNIFY_DIR = '/home/wuhiu/deeplearning/2_UnifySession/'
IMAGE_DIR = '/home/wuhiu/deeplearning/3_SessionImage/'


def getMatrixfrom_pcap(filename, width):
    with open(filename, 'rb') as f:
        content = f.read()
    hexst = binascii.hexlify(content)
    fh = numpy.array([int(hexst[i:i + 2], 16) for i in range(0, len(hexst), 2)])
    rn = len(fh) // width
    fh = numpy.reshape(fh[:rn * width], (-1, width))
    fh = numpy.uint8(fh)
    return fh


def get_one_dim_form(filename):
    with open(filename, 'rb') as f:
        content = f.read()
    hexst = binascii.hexlify(content)
    fh = numpy.array([int(hexst[i:i + 2], 16) for i in range(0, len(hexst), 2)])
    fh = fh.astype('float32')
    fh /= 255
    return fh


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def generate_image():
    for i, d in enumerate(os.listdir(UNIFY_DIR)):
        dir_full = os.path.join(IMAGE_DIR, str(i))
        mkdir_p(dir_full)
        for f in os.listdir(os.path.join(UNIFY_DIR, d)):
            bin_full = os.path.join(UNIFY_DIR, d, f)
            im = Image.fromarray(getMatrixfrom_pcap(bin_full, PNG_SIZE))
            png_full = os.path.join(dir_full, os.path.splitext(f)[0] + '.png')
            im.save(png_full)


def get_cnn_input():
    input_data = []
    for i, d in enumerate(os.listdir(UNIFY_DIR)):
        for f in os.listdir(os.path.join(UNIFY_DIR, d)):
            bin_full = os.path.join(UNIFY_DIR, d, f)
            input_data.append(get_one_dim_form(bin_full))
    print('input data: ', input_data)
    return input_data
