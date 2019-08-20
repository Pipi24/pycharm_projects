#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-3-8 下午7:09
# @Author  : Wuhiu
# @Email   : wuhiugo@163.com
# @File    : arpAnalyzer.py
# @Software: PyCharm

from pktAnalyzer import baseAnalyzer

from scapy.all import *
from scapy.utils import PcapReader


class ARPAnalyzer(baseAnalyzer.Analyzer):
    def arp_analyse(self, files_path):
        # count = 0
        for i in range(0, len(files_path)):
            try:
                packets = PcapReader(files_path[i])

                while True:
                    packet = packets.read_packet()
                    if packet is None:
                        break
                    else:
                        # count = count+1
                        print(repr(packet))
                packets.close()
            except Scapy_Exception as e:
                print(e)


if __name__ == '__main__':

    arp_analyzer = ARPAnalyzer('arp', '5', ''
                                           ''
                                           'z')
    arp_analyzer.capture_packet()
    files_path = arp_analyzer.get_file_path()
    # print(files_list)
    arp_analyzer.analyse(files_path)
