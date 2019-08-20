#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-3-8 下午7:23
# @Author  : Wuhiu
# @Email   : wuhiugo@163.com
# @File    : baseAnalyzer.py
# @Software: PyCharm

import dns
from dns import resolver
from dns import reversename
import socket


def dns(domain):
    # print(type(domain))
    ans = resolver.query(domain, 'A')
    print(ans)
    for a in ans.response.answer:
        for i in a.items:
            print(i.to_text())
            print(type(i))

def dns_socket(IP):
    # IP = socket.inet_aton(IP)
    # print(IP)
    try:
        result = socket.gethostbyname_ex(IP)
        print('Primary hostname:')
        print('  ' + result[0])

        # Display the list of available addresses that is also returned
        print('\nAddresses:')
        for item in result[2]:
            print('  ' + item)
    except socket.herror as e:
        print('Could not look up name:'), e

def rdns_socket(IP):
    # IP = socket.inet_aton(IP)
    # print(IP)
    print('rdns_socket')
    try:
        result = socket.gethostbyaddr(IP)
        print('Primary hostname:')
        print('  ' + result[0])

        # Display the list of available addresses that is also returned
        print('\nAddresses:')
        for item in result[2]:
            print('  ' + item)
    except socket.herror as e:
        print('Could not look up name:', e)


def rdns(IP):
    try:
        IP = reversename.from_address(IP)
        print(IP)
        print(type(IP))
        A = resolver.query(IP, 'PTR')  # 解析A记录类型
        print(A)
        for i in A.response.answer:
            for j in i.items:
                print(j.to_text())
                print(type(j))
    except Exception as e:
        print("dns resolver error:" + str(e))
        return None


# coding=utf-8
'''
IP反查小工具
http://dns.aizhan.com/index.php?r=index/domains&ip=202.203.208.8&page=1&_=1408264478284
'''
import requests, json, urllib, sys, os
from bs4 import BeautifulSoup


# 获取页面内容
def getPage(ip, page):
    r = requests.get("http://dns.aizhan.com/%s/" % ip)
    # print(r.text)
    print(r.url)
    return r


# 获取最大的页数
def getMaxPage(ip):
    r = getPage(ip, 1)
    if r.content:
        json_data = {}
        print(r.json())
        print(type(r.json()))
        json_data = r.json()
        maxcount = json_data[u'conut']
        maxpage = int(int(maxcount) / 20) + 1
        return maxpage


# 获取域名列表
def getDomainsList(ip):
    maxpage = getMaxPage(ip)
    result = []
    for x in range(1, maxpage + 1):
        r = getPage(ip, x)
        result.append(r.json()[u"domains"])
    return result


# 获取最终结果，形式：{url  title}  并写入文件中
def getResultWithTitle(filepath, domain_list):
    f = open(filepath, "a")
    res_dict = {'domain': '', 'title': ''}
    res_list = []
    f.write('<html>')
    for x in domain_list:
        for i in range(0, len(x)):
            title = urllib.urlopen("http://dns.aizhan.com/index.php?r=index/title&id=%d&url=%s" % (i, x[i])).read()
            soup = BeautifulSoup(title)
            res_dict['domain'] = x[i]
            res_dict['title'] = soup.contents[0].encode('utf-8')
            f.write('<a href=' + str(res_dict['domain']) + '>' + str(res_dict['domain']) + '</a>\t\t' + str(
                res_dict['title']) + '<br/>')
            res_list.append(res_dict)
    f.write('</html>')
    f.close()
    return res_list


# if __name__ == "__main__":
#     if len(sys.argv) < 3:
#         print
#         "Usage:reverseIP targetIP Outfile"
#     else:
#         ip = str(sys.argv[1])
#         print(ip)
#         print(type(ip))
#         outfile = str(sys.argv[2])
#         if not str(os.path.basename(outfile)).split('.')[-1] == 'html':
#             print
#             "The outfile must end with '.html' "
#         else:
#             print("The target IP is :%s" % ip)
#             print("Starting, please wait...")
#             domainList = getDomainsList(ip)
#             getResultWithTitle(outfile, domainList)
#             print
#             "Success! The path of result file is %s" % outfile


if __name__ == '__main__':
    #dns('www.baidu.com')
    # rdns('220.181.57.216')
    #rdns('131.202.240.87')
    rdns('113.96.208.206')
    #print()
    #rdns_socket('220.181.14.141')
    #dns_socket('www.163.com')

