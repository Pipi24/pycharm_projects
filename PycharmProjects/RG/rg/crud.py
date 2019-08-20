#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @DATE    : 19-4-23
# @Time    : 上午9:21
# @Author  : wuhiu
# @Email   : wuhiugo@163.com
# @File    : crud
# @Software: PyCharm

import datetime

from django.db import connection

from rg import models


def insert_relations(dict_ip_host, list_fields):
    obj_fields = []
    for dict_fields in list_fields:
        ip_src = dict_fields['ip_src']
        ip_dst = dict_fields['ip_dst']
        dict_fields['host_src'] = 'None'
        dict_fields['host_dst'] = 'None'
        if ip_src in dict_ip_host and ip_dst in dict_ip_host:
            dict_fields['host_src'] = dict_ip_host[ip_src]
            dict_fields['host_dst'] = dict_ip_host[ip_dst]
        elif ip_src in dict_ip_host:
            dict_fields['host_src'] = dict_ip_host[ip_src]
        elif ip_dst in dict_ip_host:
            dict_fields['host_dst'] = dict_ip_host[ip_dst]
        obj_fields.append(models.RgBaseInfo(
            timestamp=dict_fields['ts'], eth_src=dict_fields['eth_src'],
            eth_dst=dict_fields['eth_dst'], eth_type=dict_fields['eth_type'],
            ip_src=dict_fields['ip_src'], ip_dst=dict_fields['ip_dst'], ip_proto=dict_fields['ip_proto'],
            trans_sport=dict_fields['trans_sport'], trans_dport=dict_fields['trans_dport'],
            comm_way=dict_fields['comm_way'],
            host_src=dict_fields['host_src'], host_dst=dict_fields['host_dst']))

    models.RgBaseInfo.objects.bulk_create(obj_fields)
    print('insert rgbaseInfo succeed!')


def insert_ip_host(dict_ip_host):
    obj_ip_host = []
    for ip, host in dict_ip_host.items():
        obj_ip_host.append(models.IpHost(ip=ip, host=host))
    models.IpHost.objects.bulk_create(obj_ip_host)
    print('insert ip_host succeed!')


def insert_fields(list_fields):
    obj_fields = []
    for f in list_fields:
        obj_fields.append(models.FieldsInfo(timestamp=f['ts'], eth_src=f['eth_src'],
                                            eth_dst=f['eth_dst'], eth_type=f['eth_type'],
                                            ip_src=f['ip_src'], ip_dst=f['ip_dst'], ip_proto=f['ip_proto'],
                                            trans_sport=f['trans_sport'], trans_dport=f['trans_dport'],
                                            comm_way=f['comm_way']))
    models.FieldsInfo.objects.bulk_create(obj_fields)
    print('insert fields succeed!')


def join_fields_host():
    cursor = connection.cursor()
    sql = '''insert into rg_rgbaseinfo
        select 
            a.id,
            a.timestamp,
            a.eth_src, a.eth_dst, a.eth_type,
            a.ip_src, a.ip_dst, a.ip_proto,
            a.trans_sport, a.trans_dport,
            a.comm_way,
            b.host as host_src,
            c.host as host_dst
        from rg_fieldsinfo as a
        left join rg_iphost as b
        on a.ip_src = b.ip
        left join rg_iphost as c
        on a.ip_dst = c.ip'''

    cursor.execute(sql)


def query_rg_v1():
    list_rgs = []
    cursor = connection.cursor()
    sql = '''select a.timestamp, a.eth_src, a.eth_dst, a.eth_type, 
    a.ip_src, a.ip_dst, a.ip_proto,
    a.trans_sport, a.trans_dport,
    a.comm_way,
    b.host as host_src,
    c.host as host_dst
    from rg_fieldsinfo as a
    left join rg_iphost as b
    on a.ip_src = b.ip
    left join rg_iphost as c
    on a.ip_dst = c.ip'''

    cursor.execute(sql)
    raw = cursor.fetchall()
    print('raw: ', raw)
    for rg in raw:
        dict_rg = dict()
        local_time = datetime.datetime.utcfromtimestamp(rg[0]) + datetime.timedelta(hours=8)
        dict_rg['timestamp'] = local_time.strftime("%Y-%m-%d %H:%M:%S.%f")
        dict_rg['eth_src'] = rg[1]
        dict_rg['eth_dst'] = rg[2]
        dict_rg['eth_type'] = rg[3]
        dict_rg['ip_src'] = rg[4]
        dict_rg['ip_dst'] = rg[5]
        dict_rg['ip_proto'] = rg[6]
        dict_rg['trans_sport'] = rg[7]
        dict_rg['trans_dport'] = rg[8]
        dict_rg['comm_way'] = rg[9]
        dict_rg['host_src'] = rg[10]
        dict_rg['host_dst'] = rg[11]
        list_rgs.append(dict_rg)
    print('list_rgs: ', list_rgs)
    list_rgs.sort(key=lambda x: x['timestamp'], reverse=False)
    return list_rgs


def query_rg_v2():
    list_all_rgs = models.RgBaseInfo.objects.all()
    length = list_all_rgs.count()
    if length > 20:
        list_rgs = list_all_rgs[length - 20:length]
        return list_rgs
    else:
        return list_all_rgs
