#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-3-8 下午7:23
# @Author  : Wuhiu
# @Email   : wuhiugo@163.com
# @File    : baseAnalyzer.py
# @Software: PyCharm

import numpy
from PIL import Image
import binascii
import errno
import os

PNG_SIZE = 28


def getMatrixfrom_pcap(filename, width):
    with open(filename, 'rb') as f:
        content = f.read()
    hexst = binascii.hexlify(content)
    fh = numpy.array([int(hexst[i:i + 2], 16) for i in range(0, len(hexst), 2)])
    rn = len(fh) // width
    fh = numpy.reshape(fh[:rn * width], (-1, width))
    fh = numpy.uint8(fh)
    return fh


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


paths = ['/home/wuhiu/deeplearning/2_UnifySession/', '/home/wuhiu/deeplearning/3_SessionImage/']
for i, d in enumerate(os.listdir(paths[0])):
    dir_full = os.path.join(paths[1], str(i))
    mkdir_p(dir_full)
    for f in os.listdir(os.path.join(paths[0], d)):
        bin_full = os.path.join(paths[0], d, f)
        im = Image.fromarray(getMatrixfrom_pcap(bin_full, PNG_SIZE))
        png_full = os.path.join(dir_full, os.path.splitext(f)[0] + '.png')
        im.save(png_full)


