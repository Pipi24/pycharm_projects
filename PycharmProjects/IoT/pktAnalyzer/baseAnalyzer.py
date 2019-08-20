#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-3-8 下午7:23
# @Author  : Wuhiu
# @Email   : wuhiugo@163.com
# @File    : baseAnalyzer.py
# @Software: PyCharm


from scapy.all import *
from scapy.utils import PcapReader

from pktCaptureShell import pktCapture


class Analyzer:
    data_dir = "/home/wuhiu/Data/"

    def __init__(self, protocol, file_count, packet_count):
        self.protocol = protocol
        self.file_count = file_count
        self.packet_count = packet_count

    def capture_packet(self):
        pktCapture.capture(self.protocol, self.file_count, self.packet_count)

        # self.protocol = input("Please input protocol:")
        # self.file_count  = input("Please input file count:")
        # self.packet_count  = input("Please input packet count:")

    def get_file_path(self):
        data_dir = Analyzer.data_dir + self.protocol + '/'
        print("Data dir is:", data_dir)
        files_path = []

        files = os.listdir(data_dir)
        for f in files:
            file_path = data_dir + f
            print(file_path)
            if os.path.isfile(file_path):
                files_path.append(file_path)
        files_path.sort()
        print(files_path)
        return files_path

    def analyse(self, files_path):
        count = 0
        for i in range(0, len(files_path)):
            try:
                packets = PcapReader(files_path[i])

                while True:
                    packet = packets.read_packet()
                    if packet is None:
                        break
                    else:
                        count = count+1
                        print(repr(packet))
                        # print(packet['DNS'].id)
                        # for packet in packets:
                        #     print(repr(packet))
                        #     #print(type(packet))
                        #     #print(packet['CookedLinux'].src)
                        #     break
                print(count)
                packets.close()
            except Scapy_Exception as e:
                print(e)


if __name__ == "__main__":
    analyzer = Analyzer('ssdp', '1', '500')
    analyzer.capture_packet()
    files_path = analyzer.get_file_path()
    # print(files_list)
    analyzer.analyse(files_path)



# packets=rdpcap('/home/wuhiu/Data/arp100.pcap')
# for data in packets:
#     if 'ARP' in data:
#         s = repr(data)
#         print(s)

# print(sys.path)