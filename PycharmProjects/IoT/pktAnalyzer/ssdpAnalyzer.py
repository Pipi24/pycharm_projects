#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-3-8 下午7:46
# @Author  : Wuhiu
# @Email   : wuhiugo@163.com
# @File    : ssdpAnalyzer.py
# @Software: PyCharm

from pktAnalyzer import baseAnalyzer

from scapy.all import *
from scapy.utils import PcapReader


class SSDPAnalyzer(baseAnalyzer.Analyzer):
    pass


if __name__ == '__main__':

    ssdp_analyzer = SSDPAnalyzer('ssdp', '1', '100')
    ssdp_analyzer.capture_packet()
    files_path = ssdp_analyzer.get_file_path()
    # print(files_list)
    ssdp_analyzer.analyse(files_path)
