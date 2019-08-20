#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-3-8 下午7:23
# @Author  : Wuhiu
# @Email   : wuhiugo@163.com
# @File    : baseAnalyzer.py
# @Software: PyCharm

import dpkt
import socket
import datetime
from dateutil import tz
from iot.models import BinaryStore
from iot.models import FieldsInfo
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


def store_ts_binary(path):
    with open(path, 'rb') as f:
        pcaps = dpkt.pcap.Reader(f)
        for ts, buf in pcaps:
            print(ts)
            print(type(ts))
            print(buf)
            print(type(buf))
            BinaryStore.objects.create(timestamp=str(ts), binaryData=buf)


def store_fields(path):
    with open(path, 'rb') as f:  # 要以rb方式打开，用r方式打开会报错
        pkts = dpkt.pcap.Reader(f)
        # count = 0
        fields_list = []
        # s_time = datetime.datetime.now()
        for ts, raw_data in pkts:
            eth = dpkt.ethernet.Ethernet(raw_data)
            # 过滤掉没有IP段的包
            if not isinstance(eth.data, dpkt.ip.IP) and not isinstance(eth.data, dpkt.ip6.IP6):
                # if eth.type != dpkt.ethernet.ETH_TYPE_IP and eth.type != dpkt.ethernet.ETH_TYPE_IP6:
                continue
            ip = eth.data
            # 过滤掉Tcp/Udp以外的包
            if ip.p != 6 and ip.p != 17:
                continue
            t_l = ip.data
            a_l = t_l.data
            # 过滤掉没有应用层数据的包
            # if len(a_l) is 0:
            #     continue
            fields_list.append(FieldsInfo(timestamp=ts, eth_src=eth.src, eth_dst=eth.dst, eth_type=eth.type,
                                          ip_src=ip.src, ip_dst=ip.dst, ip_proto=ip.p,
                                          trans_sport=t_l.sport, trans_dport=t_l.dport))
            # count += 1
            # print(count)
        FieldsInfo.objects.bulk_create(fields_list)
        # e_time = datetime.datetime.now()
        # diff = e_time - s_time
        # print(diff)
        # print(diff.total_seconds())
        # print(diff / count)


def get_fields():
    fields = FieldsInfo.objects.all()[0:10000]
    print(fields)
    # # 得到本地时区名字
    # to_zone_name = datetime.datetime.now(tz.tzlocal()).tzname()
    # print(to_zone_name)
    # from_zone = tz.gettz('UTC')
    # print(from_zone)
    # to_zone = tz.gettz(to_zone_name)
    # print(to_zone)
    for o in fields:
        local_time = datetime.datetime.utcfromtimestamp(o.timestamp)+datetime.timedelta(hours=8)
        o.timestamp = local_time.strftime("%Y-%m-%d %H:%M:%S.%f")

        o.eth_src = mac_addr(o.eth_src)
        o.eth_dst = mac_addr(o.eth_dst)
        if o.eth_type == int(dpkt.ethernet.ETH_TYPE_IP):
            o.eth_type = 'IPv4'
        elif o.eth_type == int(dpkt.ethernet.ETH_TYPE_IP6):
            o.eth_type = 'IPv6'

        o.ip_src = inet_to_str(o.ip_src)
        o.ip_dst = inet_to_str(o.ip_dst)
        if o.ip_proto == 6:
            o.ip_proto = 'TCP'
        elif o.ip_proto == 17:
            o.ip_proto = 'UDP'
    return fields


if __name__ == '__main__':
    path = '/home/wuhiu/deeplearning/VPNData/non-vpn/Chat/AIMchat1.pcap'
    store_ts_binary(path)


