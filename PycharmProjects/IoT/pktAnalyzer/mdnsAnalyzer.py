#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-3-8 下午7:44
# @Author  : Wuhiu
# @Email   : wuhiugo@163.com
# @File    : mdnsAnalyzer.py
# @Software: PyCharm

from pktAnalyzer import baseAnalyzer

from scapy.all import *
from scapy.utils import PcapReader


class MDNSAnalyzer(baseAnalyzer.Analyzer):
    pass


if __name__ == '__main__':

    mdns_analyzer = MDNSAnalyzer('mdns', '1', '100')
    mdns_analyzer.capture_packet()
    files_path = mdns_analyzer.get_file_path()
    # print(files_list)
    mdns_analyzer.analyse(files_path)
