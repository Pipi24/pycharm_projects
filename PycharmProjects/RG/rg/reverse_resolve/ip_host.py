#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @DATE    : 19-4-23
# @Time    : 下午1:54
# @Author  : wuhiu
# @Email   : wuhiugo@163.com
# @File    : ip_host
# @Software: PyCharm

import subprocess


def get_ip_host(path):
    dict_ip_host = {}
    obj = subprocess.Popen(['tshark', '-r', path, '-z', 'hosts', '-q'],
                           shell=False, stdout=subprocess.PIPE)
    # print(len(a))
    # print(a.communicate())
    output = str(obj.stdout.read())
    obj.stdout.close()
    ip_host_list = output.split('\\n\\n')[1].split('\\n')[0:-1]
    for i in ip_host_list:
        dict_ip_host[i.split('\\t')[0]] = i.split('\\t')[1]
    print('dict_ip_host : ', dict_ip_host)
    return dict_ip_host


if __name__ == '__main__':
    get_ip_host('/home/wuhiu/deeplearning/VPNData/non-vpn/Chat/AIMchat1.pcap')
