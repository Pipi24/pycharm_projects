#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-3-8 下午7:23
# @Author  : Wuhiu
# @Email   : wuhiugo@163.com
# @File    : baseAnalyzer.py
# @Software: PyCharm
import os
import dpkt
import socket
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


def get_pcaps_path(dataset_root_dir_path):
    dirs_name = os.listdir(dataset_root_dir_path)
    # print(dirs_name)
    pcaps_path = []
    for dir_name in dirs_name:
        # print(dir_name)
        dir_path = os.path.join(dataset_root_dir_path, dir_name)
        # print(dir_path)
        class_dirs_name = os.listdir(dir_path)
        # print(class_dirs_name)
        for class_dir_name in class_dirs_name:
            class_dir_path = os.path.join(dir_path, class_dir_name)
            # print(class_dir_path)
            pcaps_name = os.listdir(class_dir_path)
            for pcap_name in pcaps_name:
                name, ext = os.path.splitext(pcap_name)
                if ext == '.pcap':
                    print(pcap_name)
                    pcap_path = os.path.join(class_dir_path, pcap_name)
                # print(pcap_path)
                    pcaps_path.append(pcap_path)
    # print(pcaps_path)
    print(len(pcaps_path))
    return pcaps_path


def parse_pcap_file(path):
    with open(path, 'rb') as f:  # 要以rb方式打开，用r方式打开会报错
        pkts = dpkt.pcap.Reader(f)
        count = 0
        # print(pkts)
        for ts, raw_data in pkts:
            # layers_fields = {}
            # timestamp = {}
            # eth_layers_fields = {}
            # ip_layers_fields = {}
            # trans_layers_fields = {}
            # timestamp['timestamp'] = ts
            # layers_fields['Timestamp'] = timestamp
            # print(raw_data)
            # print(len(raw_data))
            eth = dpkt.ethernet.Ethernet(raw_data)
            # 这里也是对没有IP段的包过滤掉
            if not isinstance(eth.data, dpkt.ip.IP) and not isinstance(eth.data, dpkt.ip6.IP6):
                # if eth.type != dpkt.ethernet.ETH_TYPE_IP and eth.type != dpkt.ethernet.ETH_TYPE_IP6:
                continue
            ip = eth.data
            if ip.p is not 6 and 17:
                continue
            trans_layer = ip.data
            app_layer = trans_layer.data
            if len(app_layer) is 0:
                continue
            # print(eth)
            # print(len(eth))
            print(eth.src)
            print(type(eth.src))
            print(len(eth.src))
            sda = mac_addr(eth.src)
            print(sda)
            print(type(sda))
            print(len(sda))
            print(type(eth.type))
            # print('Ethernet Frame: ', mac_addr(eth.src), mac_addr(eth.dst), '0x%04x' % eth.type, len(eth))

            # eth_layers_fields['Src'] = mac_addr(eth.src)
            # eth_layers_fields['Dst'] = mac_addr(eth.dst)
            # eth_layers_fields['Type'] = eth.type
            # layers_fields['Ethernet'] = eth_layers_fields
            #
            # ip_layers_fields['Src'] = inet_to_str(ip.src)
            # ip_layers_fields['Dst'] = inet_to_str(ip.dst)
            print(ip.src)
            print(type(ip.src))
            print(len(ip.src))
            sd = inet_to_str(ip.src)
            print(sd)
            print(type(sd))
            print(len(sd))
            # ip_layers_fields['Proto'] = ip.p
            # layers_fields['IP'] = ip_layers_fields
            #
            # trans_layers_fields['Sport'] = trans_layer.sport
            # trans_layers_fields['Dport'] = trans_layer.dport
            # layers_fields['Trans'] = trans_layers_fields
            # print(layers_fields)
            break


if __name__ == '__main__':
    # parse_pcap_file('/home/wuhiu/deeplearning/VPNData/non-vpn/Chat/AIMchat1.pcap')
    pcaps_path = get_pcaps_path('/home/wuhiu/deeplearning/VPNData')
    for pcap_path in pcaps_path:
        name, ext = os.path.splitext(pcap_path)
        name += '_pre_data'
        print(name, ext)
        file = name.split('/')
        xx = file[5] + '_' + file[6]
        print(xx)
        break
