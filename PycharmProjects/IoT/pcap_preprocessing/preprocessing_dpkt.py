#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-3-8 下午7:23
# @Author  : Wuhiu
# @Email   : wuhiugo@163.com
# @File    : baseAnalyzer.py
# @Software: PyCharm

import binascii
import datetime
import os
import socket

import dpkt
import numpy as np
from PIL import Image


def inet_to_str(inet):
    try:
        return socket.inet_ntop(socket.AF_INET, inet)
    except ValueError:
        return socket.inet_ntop(socket.AF_INET6, inet)


np.set_printoptions(threshold=np.inf)


def get_pcaps_path_copy(dir_path):
    # dirs_name = os.listdir(dataset_root_dir_path)
    # print(dirs_name)
    pcaps_path = []
    # for dir_name in dirs_name:
    #     # print(dir_name)
    #     dir_path = os.path.join(dataset_root_dir_path, dir_name)
    # print(dir_path)
    pcaps_name = os.listdir(dir_path)
    # print(class_dirs_name)
    # for class_dir_name in class_dirs_name:
    #     class_dir_path = os.path.join(dir_path, class_dir_name)
    #     # print(class_dir_path)
    # pcaps_name = os.listdir(class_dir_path)
    for pcap_name in pcaps_name:
        # print(pcap_name)
        name, ext = os.path.splitext(pcap_name)
        if ext == '.pcap':
            pcap_path = os.path.join(dir_path, pcap_name)
            print(pcap_path)
            pcaps_path.append(pcap_path)
    # print(pcaps_path)
    print('pcaps_path len is: ', len(pcaps_path))
    return pcaps_path


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
                # print(pcap_name)
                name, ext = os.path.splitext(pcap_name)
                if ext == '.pcap':
                    pcap_path = os.path.join(class_dir_path, pcap_name)
                    print(pcap_path)
                    pcaps_path.append(pcap_path)
    # print(pcaps_path)
    pcaps_path.sort()
    print(pcaps_path)
    print('pcaps_path len is: ', len(pcaps_path))
    return pcaps_path


def divide_traffic_by_session(pcap_path):
    sessions = {}
    with open(pcap_path, 'rb') as f:
        pkts = dpkt.pcap.Reader(f)
        for ts, data in pkts:
            eth = dpkt.ethernet.Ethernet(data)

            # 这里也是对没有IP段的包过滤掉
            if not isinstance(eth.data, dpkt.ip.IP) and not isinstance(eth.data, dpkt.ip6.IP6):
                continue

            ip = eth.data
            if ip.p != 6 and ip.p != 17:
                continue
            trans_layer = ip.data
            ap = trans_layer.data
            if len(ap) is 0:
                continue

            ip_src = inet_to_str(ip.src)
            ip_dst = inet_to_str(ip.dst)
            # print(ip_src + '-->' + ip_dst)
            forward_quintuple = ip_src + ':' + \
                                str(trans_layer.sport) + '-->' + \
                                ip_dst + ':' + \
                                str(trans_layer.dport) + ' ' + \
                                str(ip.p)
            # print(forward_quintuple)
            reverse_quintuple = ip_dst + ':' + \
                                str(trans_layer.dport) + '-->' + \
                                ip_src + ':' + \
                                str(trans_layer.sport) + ' ' + \
                                str(ip.p)
            if forward_quintuple in sessions:
                sessions[forward_quintuple] += data
            elif reverse_quintuple in sessions:
                sessions[reverse_quintuple] += data
            else:
                sessions[forward_quintuple] = data
    # print('pcap_path is: ', pcap_path)
    too_short = [key for key, value in sessions.items() if len(value) < 512]
    for key in too_short:
        del sessions[key]
    print('sessions len is: ', len(sessions))
    return sessions


def unify_sessions(sessions, length):
    byte_sessions = []
    for quintuple, binary_session in sessions.items():
        hex_session = binascii.hexlify(binary_session)
        byte_session = np.array([int(hex_session[i:i + 2], 16) for i in range(0, len(hex_session), 2)])
        len_byte_session = len(byte_session)
        diff = len_byte_session - length
        if diff < 0:
            padding = np.full(abs(diff), int('0x00', 16))
            byte_session = np.concatenate((byte_session, padding))
        else:
            byte_session = byte_session[0:length]
        byte_session = np.uint8(byte_session)
        byte_sessions.append(byte_session)
    print('byte_sessions len is: ', len(byte_sessions))
    return byte_sessions


def generate_traffic_images(byte_sessions, width, store_path):
    base_path = '/home/wuhiu/deeplearning/traffic image/'
    path_split = store_path.split('/')
    path = base_path + path_split[6]
    count = 0
    for byte_session in byte_sessions:
        quotient = len(byte_session) // width
        # print(rn)
        byte_session = np.reshape(byte_session[:quotient * width], (-1, width))
        byte_session = np.uint8(byte_session)
        im = Image.fromarray(byte_session)
        im.save(path + '/' + path_split[7] + '_img%d.png' % count)
        count += 1


def generate_trffic_bytes_files(byte_sessions, store_path):
    len_byte_sessions = len(byte_sessions)

    data_store_path = store_path + '_data'
    with open(data_store_path, 'wb') as f:
        for byte_session in byte_sessions:
            # str_session = str(byte_session)
            f.write(byte_session)
            # print(byte_session)
            # print(type(byte_session))

    path_split = store_path.split('/')
    # print(path_split)
    pcap_label = path_split[5] + '_' + path_split[6] + ','
    print('pcap_label is: ', pcap_label)
    label = ''
    label_store_path = store_path + '_label'
    with open(label_store_path, 'w') as f:
        for i in range(len_byte_sessions):
            label += pcap_label
        print('label is: ', label)
        print('label len is: ', len(label) / len(pcap_label))
        f.write(label)


def generate_dataset():
    SEQ_LEN = 784
    # pcaps_path = get_pcaps_path('/home/wuhiu/deeplearning/VPNData')
    DIR_PATH = '/home/wuhiu/deeplearning/VPNData/non-vpn/Chat'
    pcaps_path = get_pcaps_path_copy(DIR_PATH)

    count = 0
    input("Start")
    for pcap_path in pcaps_path:
        s_time = datetime.datetime.now()
        print(s_time)
        print('pcap_path is: ', pcap_path)
        sessions = divide_traffic_by_session(pcap_path)
        byte_sessions = unify_sessions(sessions, SEQ_LEN)
        path, ext = os.path.splitext(pcap_path)
        # print(path, ext)
        # print(path)
        generate_trffic_bytes_files(byte_sessions, path)
        e_time = datetime.datetime.now()
        print(e_time)
        diff = e_time - s_time
        print(diff)
        print(diff.total_seconds())
        input('Continue!')
    print("Done!")


def generate_traffic_image():
    DIR_PATH = '/home/wuhiu/deeplearning/VPNData/non-vpn/Chat/'
    # PCAP_PATH = '/home/wuhiu/deeplearning/VPNData/non-vpn/Chat/skype_file1.pcap'
    SEQ_LEN = 784
    WIDTH = 28
    pcaps_path = get_pcaps_path_copy(DIR_PATH)
    for pcap_path in pcaps_path:
        print('pcap_path is: ', pcap_path)
        sessions = divide_traffic_by_session(pcap_path)
        byte_sessions = unify_sessions(sessions, SEQ_LEN)
        path, ext = os.path.splitext(pcap_path)
        generate_traffic_images(byte_sessions, WIDTH, path)
    print("Done!")


if __name__ == '__main__':
    # generate_dataset()
    # generate_traffic_image()

    SEQ_LEN = 784
    # pcaps_path = get_pcaps_path('/home/wuhiu/deeplearning/VPNData')
    DIR_PATH = '/home/wuhiu/deeplearning/VPNData/non-vpn/Chat'
    pcaps_path = get_pcaps_path_copy(DIR_PATH)

    count = 0
    input("Start")
    for pcap_path in pcaps_path:
        s_time = datetime.datetime.now()
        print(s_time)
        print('pcap_path is: ', pcap_path)
        sessions = divide_traffic_by_session(pcap_path)
        byte_sessions = unify_sessions(sessions, SEQ_LEN)
