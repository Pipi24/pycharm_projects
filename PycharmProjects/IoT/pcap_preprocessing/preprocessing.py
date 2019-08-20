#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-3-8 下午7:23
# @Author  : Wuhiu
# @Email   : wuhiugo@163.com
# @File    : baseAnalyzer.py
# @Software: PyCharm

from scapy.all import *
from scapy.utils import PcapReader
# from pktAnalyzer import baseAnalyzer
#
# test = baseAnalyzer.Analyzer
# print(test)

def divide_traffic_by_session(files_path):
    num_pkgs_session = {}
    session_data = ()
    try:
        packets = PcapReader(files_path)
        count = 0
        while True:
            packet = packets.read_packet()
            if packet is None:
                break
            elif 'IP' in packet and ('UDP' in packet or 'TCP' in packet):
                try:

                    # print(type(packet[1].src))
                    # print(packet[1].dst)
                    # print(type(packet[1].proto))
                    # print(type(packet[2].sport))
                    # print(packet[2].dport)
                    forward_quintuple = packet[1].src + ':' + \
                        str(packet[2].sport) + '-->' + \
                        packet[1].dst + ':' + \
                        str(packet[2].dport) + ' ' + \
                        str(packet[1].proto)

                    reverse_quintuple = packet[1].dst + ':' + \
                        str(packet[2].dport) + '-->' + \
                        packet[1].src + ':' + \
                        str(packet[2].sport) + ' ' + \
                        str(packet[1].proto)
                    print(forward_quintuple)
                    # print(reverse_quintuple)
                    print(repr(packet))
                    # print("%r") % packet
                    print(len(packet))
                    print(type(packet))
                    packet = bytes(packet)
                    print(type(packet))
                    print(packet)

                    if forward_quintuple in num_pkgs_session:
                        num_pkgs_session[forward_quintuple] += packet
                    elif reverse_quintuple in num_pkgs_session:
                        num_pkgs_session[reverse_quintuple] += packet
                    else:
                        num_pkgs_session[forward_quintuple] = packet



                    # print(repr(packet))
                    # num_pkgs_session[forword_quintuple] = 0
                    count += 1
                except AttributeError:
                    continue
        for p in num_pkgs_session.items():
            print(p)
        packets.close()
    except Scapy_Exception as e:
        print(e)


if __name__ == "__main__":
    divide_traffic_by_session('/home/wuhiu/AIMchat1.pcap')
