#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @DATE    : 19-4-24
# @Time    : 上午10:49
# @Author  : wuhiu
# @Email   : wuhiugo@163.com
# @File    : call2
# @Software: PyCharm

import shutil


from preprocess import pcap2sess
from preprocess import process_sess
from preprocess import sess2field
from preprocess import sess2input
from reverse_resolve import ip_host
from call import call1
IS_CLASSIFY_TRAFFIC = False
dict_6class_novpn = {0: 'non-vpn_Chat', 1: 'non-vpn_Email', 2: 'non-vpn_File Transfer',
                     3: 'non-vpn_P2P', 4: 'non-vpn_Streaming', 5: 'non-vpn_VoIP'}


def call_all():
    for i in range(2):
        list_fields = call1.call_all()
    print(list_fields)

if __name__ == '__main__':
    call_all()
