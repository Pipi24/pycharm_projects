#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @DATE    : 19-4-23
# @Time    : 下午2:13
# @Author  : wuhiu
# @Email   : wuhiugo@163.com
# @File    : pcap2sess
# @Software: PyCharm

import os
import subprocess

from preprocess_iot.sess2field import get_files_path

SPLIT_TOOL = '/home/wuhiu/deeplearning/SplitCap_2-1/SplitCap.exe'
SPLIT_BASE_PATH = '/home/wuhiu/deeplearning/1_SplitPcap/'


def split_pcap(path):
    file = os.path.split(path)[1]
    filename = os.path.splitext(file)[0]
    split_path = SPLIT_BASE_PATH + filename
    p = subprocess.Popen(args=['mono', SPLIT_TOOL, '-p', '60000', '-b', '60000', '-r', path, '-o', split_path],
                         shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(p.communicate())
    print(split_path)
    # get_files_path(split_path)


if __name__ == '__main__':
    split_pcap('/home/wuhiu/deeplearning/VPNData/non-vpn/Chat/AIMchat1.pcap')
