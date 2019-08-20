#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-3-8 下午7:23
# @Author  : Wuhiu
# @Email   : wuhiugo@163.com
# @File    : baseAnalyzer.py
# @Software: PyCharm

import subprocess

SHELL_PATH = '/home/wuhiu/deeplearning/pcap2sess.sh'


def call_shell(pcap_path):
    print("Call Start.")
    p = subprocess.Popen(args=[SHELL_PATH, pcap_path],
                         shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(p.communicate())
    print("Call End.")


if __name__ == '__main__':
    call_shell('/home/wuhiu/deeplearning/VPNData/non-vpn/Chat/AIMchat1.pcap')
