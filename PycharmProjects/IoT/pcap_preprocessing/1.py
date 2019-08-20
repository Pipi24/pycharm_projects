#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-3-8 下午7:23
# @Author  : Wuhiu
# @Email   : wuhiugo@163.com
# @File    : baseAnalyzer.py
# @Software: PyCharm

import dns.resolver

# if __name__=="__main__":
#     domain = 'mx1.qq.com'
#     NS = dns.resolver.query(domain, 'NS')
#     for i in NS.response.answer:
#         for j in i.items:
#             print(j.to_text())
#
# if __name__=="__main__":
#     domain = '163.com'
#     CNAME = dns.resolver.query(domain, 'CNAME')
#     for i in CNAME.response.answer:
#         for j in i.items:
#             print(j.to_text())
if __name__ == "__main__":
    domain = 'mx1.qq.com'
    CNAME = dns.resolver.query(domain, 'A')
    for i in CNAME.response.answer:
        for j in i.items:
            print(j.to_text())
# domain = input('Please input an domain: ')
#
# MX = dns.resolver.query(domain, 'MX')
# for i in MX:
#     print('MX preference =', i.preference, 'mail exchanger =', i.exchange)