#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @DATE    : 19-4-24
# @Time    : 上午9:56
# @Author  : wuhiu
# @Email   : wuhiugo@163.com
# @File    : call
# @Software: PyCharm

import shutil
from preprocess import cnn_predict
from preprocess import pcap2sess
from preprocess import process_sess
from preprocess import sess2field
from preprocess import sess2input
from reverse_resolve import ip_host

IS_CLASSIFY_TRAFFIC = True
dict_6class_novpn = {0: 'non-vpn_Chat', 1: 'non-vpn_Email', 2: 'non-vpn_File Transfer',
                     3: 'non-vpn_P2P', 4: 'non-vpn_Streaming', 5: 'non-vpn_VoIP'}


def call_all():
    path = '/home/wuhiu/deeplearning/VPNData/non-vpn/Chat/AIMchat1.pcap'
    dict_ip_host = ip_host.get_ip_host(path)
    split_dir = pcap2sess.split_pcap(path)
    unify_dir = process_sess.unify_sess(split_dir)
    list_fields = sess2field.get_field(unify_dir)

    # get fields and communication way from pcap
    if IS_CLASSIFY_TRAFFIC:
        x_pred = sess2input.get_cnn_input(unify_dir)
        preds = cnn_predict.predict(x_pred)
        print(preds)
        for i, fields in enumerate(list_fields):
            fields['comm_way'] = dict_6class_novpn[preds[i]]
    print(list_fields)
    # shutil.rmtree(split_dir)
    # shutil.rmtree(unify_dir)


if __name__ == '__main__':
    call_all()
