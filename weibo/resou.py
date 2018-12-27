#!/usr/bin/python
#-*- coding: UTF-8 -*-
#coding=utf-8
import requests
import os
import sys
import json
import random
import cookielib
import urllib
import re
import base64
import rsa
import binascii
import time
import datetime
import MySQLdb
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding("utf-8")
'''
USER_AGENTS 随机头信息
'''
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]
# 请求超时时间
REQUEST_TIME_OUT = 10
"""
reuqst请求发送
:param url: 需要请求的url
"""
def request_url(url='',method='',data=''):
    HEADER = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection':'keep-alive',
    }
    #返回内容
    result_text = '请求错误'
    try:
        if 'get' in method:
           # rs = requests.get(url, data=data, headers=HEADER, timeout=REQUEST_TIME_OUT,proxies=ip_proexy)
            rs = requests.get(url, data=data, headers=HEADER, timeout=REQUEST_TIME_OUT)
            #time.sleep(1)
            if rs.status_code == 200:
                result_text = rs.text
        if 'post' in method:
            #rs = requests.post(url, data=data, headers=HEADER, timeout=REQUEST_TIME_OUT,proxies=ip_proexy)
            rs = requests.get(url, data=data, headers=HEADER, timeout=REQUEST_TIME_OUT)
            if rs.status_code == 200:
                result_text = rs.text
    except Exception, e:
        pass
    return result_text

def get_resuo():
    flag_bool = True
    i = 1
    while flag_bool:
        flag_bool = False
        try:
            print 'start get data num -->',i
            url = 'http://s.weibo.com/top/summary'
            text = request_url(url, 'get')
            json_data_arr = re.findall('{.{20,}}', text)
            json_data_len_dict = {}
            for index, json_data in enumerate(json_data_arr):
                json_data_len_dict[len(json_data)] = index
            keys = json_data_len_dict.keys()
            keys.sort()
            json_data = json_data_arr[json_data_len_dict[keys[-1]]]
            json_dict = json.loads(json_data)
            html_content = json_dict['html']
            soup = BeautifulSoup(html_content, 'lxml')
            tr_arr = soup.find_all('tr', attrs={'action-type': 'hover'})
            resou_arr = []
            # 提取信息
            for tr in tr_arr:
                if 5 == len(tr.find_all('td')):
                    resou_dict = {}
                    rank = tr.find_all('td')[0].string
                    resou_name = tr.find_all('td')[1].find('a').string
                    resou_dict['name'] = resou_name
                    rank = tr.find_all('td')[0].string
                    resou_dict['rank'] = rank
                    flag_node = tr.find_all('td')[1].find('i')
                    flag = ''
                    if flag_node:
                        flag = flag_node.string
                    resou_dict['flag'] = flag
                    total = tr.find_all('td')[2].text
                    resou_dict['total'] = total
                    resou_arr.append(resou_dict)
            if len(resou_arr) == 50:
                # 数据插入
                insert_resou(resou_arr)
            else:
                flag_bool = True
        except Exception,e:
            print e
            flag_bool = True
            i += 1

def insert_resou(resou_arr):
    connection = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', db='test1',charset='utf8')
    cursor = connection.cursor()
    # 删除数据
    sql = "DELETE FROM resou "
    cursor.execute(sql)
    connection.commit()
    print 'delete resou table ok -->',datetime.datetime.now()
    for dict_data in resou_arr:
        name = dict_data['name']
        rank = dict_data['rank']
        flag = dict_data['flag']
        total = dict_data['total']
        sql = "INSERT INTO resou VALUES (DEFAULT ,'"+rank+"','"+name+"','"+flag+"','"+total+"',NOW(),NOW())"
        cursor.execute(sql)
        connection.commit()
        sql = "INSERT INTO resou_history VALUES (DEFAULT ,'"+rank+"','"+name+"','"+flag+"','"+total+"',NOW(),NOW())"
        cursor.execute(sql)
        connection.commit()
    print 'resou insert into data ok! -->',(datetime.datetime.now())
    cursor.close()
    connection.close()

if __name__ == '__main__':
    print 'start up -->',datetime.datetime.now()
    while True:
        get_resuo()
        sleep_time = random.randint(120, 180)
        # 睡眠时间
        print 'start sleep,sleep time -->'+str(sleep_time)
        time.sleep(sleep_time)