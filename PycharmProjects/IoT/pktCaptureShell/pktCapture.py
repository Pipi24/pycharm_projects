#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-3-8 下午7:30
# @Author  : Wuhiu
# @Email   : wuhiugo@163.com
# @File    : pktCapture.py
# @Software: PyCharm

import subprocess


def capture(protocol, file_count, packet_count):
    shell_path = '/home/wuhiu/Code/' + protocol + 'Cap.exp'
    # print(shell_path)
    print("Capture Start.")
    p = subprocess.Popen(args=['/usr/bin/expect', shell_path, protocol, file_count, packet_count],
                         shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # p.wait()
    p.communicate()
    print("Capture End.")


if __name__ == '__main__':
    capture('ssdp', '5', '100')
