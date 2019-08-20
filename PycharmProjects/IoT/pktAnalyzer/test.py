#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-3-18 下午8:09
# @Author  : Wuhiu
# @Email   : wuhiugo@163.com
# @File    : test.py
# @Software: PyCharm


# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @DATE    : 19-4-23
# @Time    : 下午2:51
# @Author  : wuhiu
# @Email   : wuhiugo@163.com
# @File    : pcap2sess
# @Software: PyCharm

import subprocess


def get_ip_host(path):
    dict_ip_host = {}
    obj = subprocess.Popen(['tshark', '-r', path, '-z', 'io,stat,0', '-q'],
                           shell=False, stdout=subprocess.PIPE)
    # print(len(a))
    # print(a.communicate())
    output = str(obj.stdout.read())
    obj.stdout.close()
    print(output)
    output = output.split('|')
    frame = output[-3].strip()
    if frame == '\\n':
        num_frame = 1
    else:
        num_frame = int(frame)


if __name__ == '__main__':
    # get_ip_host('/home/wuhiu/deeplearning/VPNData/non-vpn/Chat/AIMchat1.pcap')
    get_ip_host(
        '/home/wuhiu/deeplearning/1_SplitPcap/email1a/email1a.pcap.UDP_131-202-240-93_60282_255-255-255-255_10505.pcap')
