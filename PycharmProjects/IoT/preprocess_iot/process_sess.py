#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-3-8 下午7:23
# @Author  : Wuhiu
# @Email   : wuhiugo@163.com
# @File    : baseAnalyzer.py
# @Software: PyCharm

import os
import errno

UNIFY_DIR = '/home/wuhiu/deeplearning/2_UnifySession/'
UNIFY_LENGTH = 784


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def unify_sess(split_path):
    dir = os.path.split(split_path)[1]
    print(dir)
    files = os.listdir(split_path)
    unify_dir = os.path.join(UNIFY_DIR, dir)
    mkdir_p(unify_dir)
    for file in files:
        file_path = os.path.join(split_path, file)
        print(file)
        with open(file_path, 'rb') as r:
            content = r.read()
            diff = len(content) - UNIFY_LENGTH
            if diff >= 0:
                content = content[0:UNIFY_LENGTH]
            else:
                padding = bytes('\x00'.encode('utf-8')) * abs(diff)
                content = content + padding
            unify_path = os.path.join(unify_dir, file)
            with open(unify_path, 'wb') as w:
                w.write(content)


if __name__ == '__main__':
    split_path = '/home/wuhiu/deeplearning/1_SplitPcap/AIMchat1'
    unify_sess(split_path)
