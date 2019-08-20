#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @DATE    : 19-4-23
# @Time    : 下午2:51
# @Author  : wuhiu
# @Email   : wuhiugo@163.com
# @File    : pcap2sess
# @Software: PyCharm

import errno
import os
import subprocess

SPLIT_TOOL = '/home/wuhiu/deeplearning/SplitCap_2-1/SplitCap.exe'
SPLIT_BASE_PATH = '/home/wuhiu/deeplearning/1_SplitPcap/'
IS_CLASSIFY_TRAFFIC = False


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def split_pcap(path):
    file = os.path.split(path)[1]
    filename = os.path.splitext(file)[0]
    split_dir = SPLIT_BASE_PATH + filename
    mkdir_p(split_dir)
    print("split dir: ", split_dir)
    p = subprocess.call(args=['mono', SPLIT_TOOL, '-p', '60000', '-b', '60000', '-r', path, '-o', split_dir],
                        shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # delete pcap files which size is smaller than 512 bytes
    # split_files = os.listdir(split_dir)
    # for file in split_files:
    #     if os.path.getsize(os.path.join(split_dir, file)) < 512:
    #         os.remove(os.path.join(split_dir, file))
    return split_dir


def filter_lack_pcap(split_dir):
    split_files = os.listdir(split_dir)
    for file in split_files:
        obj = subprocess.Popen(['tshark', '-r', os.path.join(split_dir, file), '-z', 'io,stat,0', '-q'],
                               shell=False, stdout=subprocess.PIPE)
        output = str(obj.stdout.read())
        obj.stdout.close()

        print(file)
        output = output.split('|')
        frame = output[-3].strip()
        if frame == '\\n':
            num_frame = 1
        else:
            num_frame = int(frame)
        if num_frame < 10:
            os.remove(os.path.join(split_dir, file))


if __name__ == '__main__':
    split_pcap('/home/wuhiu/deeplearning/VPNData/non-vpn/Chat/AIMchat1.pcap')
