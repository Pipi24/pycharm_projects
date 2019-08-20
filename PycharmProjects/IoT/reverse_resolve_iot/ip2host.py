#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @DATE    : 19-4-22
# @Time    : 下午4:19
# @Author  : wuhiu
# @Email   : wuhiugo@163.com
# @File    : ip2host
# @Software: PyCharm

import subprocess
ip_host = {}
obj = subprocess.Popen(['tshark', '-r', '/home/wuhiu/deeplearning/VPNData/non-vpn/Email/email1a.pcap', '-z', 'hosts', '-q'],
                       shell=False, stdout=subprocess.PIPE)
# print(len(a))
# print(a.communicate())
output = str(obj.stdout.read())
obj.stdout.close()
ip_host_list = output.split('\\n\\n')[1].split('\\n')[0:-1]
for i in ip_host_list:
    ip_host[i.split('\\t')[0]] = i.split('\\t')[1]

print(ip_host)
for k, v in ip_host.items():
    print(type(k))
    print()
    print(type(v))

