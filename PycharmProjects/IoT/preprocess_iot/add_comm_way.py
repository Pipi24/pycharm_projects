#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @DATE    : 19-4-24
# @Time    : 上午9:11
# @Author  : wuhiu
# @Email   : wuhiugo@163.com
# @File    : add_comm_way
# @Software: PyCharm
dict_classes = {0: 'chat', 1: 'email'}
a = [{'ts': 1.1, 'src': '1.1.1.1', 'comm_way': 'unknown'}, {'ts': 2.2, 'src': '2.2.2.2'}]
b = [0, 1]
for i, d in enumerate(a):
    d['comm_way'] = dict_classes[b[i]]

print(a)
