#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @DATE    : 19-4-23
# @Time    : 下午2:59
# @Author  : wuhiu
# @Email   : wuhiugo@163.com
# @File    : sess2field
# @Software: PyCharm


import os
import socket

import dpkt
from dpkt.compat import compat_ord


def mac_addr(address):
    """Convert a MAC address to a readable/printable string

       Args:
           address (str): a MAC address in hex form (e.g. '\x01\x02\x03\x04\x05\x06')
       Returns:
           str: Printable/readable MAC address
    """
    return ':'.join('%02x' % compat_ord(b) for b in address)


def inet_to_str(inet):
    """Convert inet object to a string

        Args:
            inet (inet struct): inet network address
        Returns:
            str: Printable/readable IP address
    """
    # First try ipv4 and then ipv6
    try:
        return socket.inet_ntop(socket.AF_INET, inet)
    except ValueError:
        return socket.inet_ntop(socket.AF_INET6, inet)


def get_field(files_path):
    files_path.sort()
    print(files_path)
    list_fields = []
    for file_path in files_path:
        dict_fields = {}
        with open(file_path, 'rb') as f:  # 要以rb方式打开，用r方式打开会报错
            pkts = dpkt.pcap.Reader(f)
            for ts, raw_data in pkts:
                eth = dpkt.ethernet.Ethernet(raw_data)
                ip = eth.data
                trans = ip.data

                dict_fields['eth_src'] = mac_addr(eth.src)
                dict_fields['eth_dst'] = mac_addr(eth.dst)
                if eth.type == int(dpkt.ethernet.ETH_TYPE_IP):
                    dict_fields['eth_type'] = 'IPv4'
                elif eth.type == int(dpkt.ethernet.ETH_TYPE_IP6):
                    dict_fields['eth_type'] = 'IPv6'

                dict_fields['ip_src'] = inet_to_str(ip.src)
                dict_fields['ip_dst'] = inet_to_str(ip.dst)
                if ip.p == 6:
                    dict_fields['ip_proto'] = 'TCP'
                elif ip.p == 17:
                    dict_fields['ip_proto'] = 'UDP'

                dict_fields['trans_sport'] = trans.sport
                dict_fields['trans_dport'] = trans.dport
                dict_fields['comm_way'] = 'Unknown'
                list_fields.append(dict_fields)
                break
    print(list_fields)
    print(len(list_fields))


def get_files_path(split_path):
    files_path = []
    files = os.listdir(split_path)
    for file in files:
        files_path.append(os.path.join(split_path, file))
    get_field(files_path)


if __name__ == '__main__':
    get_files_path('/home/wuhiu/deeplearning/1_SplitPcap/AIMchat1')
