#!/usr/bin/python
#-*- coding: UTF-8 -*-
#coding=utf-8
from wxpy import *
from time import sleep
import time
import requests
import random
import MySQLdb
import json
import datetime
import threading
import thread

def get_keywords(keywords_path = ''):
    file_info = open(keywords_path,'r')
    lines = file_info.readlines()
    msg_list = []
    for line in lines:
        line = line.replace('\n','').replace('\t','').replace('\r','')
        if line:
            msg_list.append(line)
    file_info.close()
    return msg_list

# 关键字比对
def keywords_to(msg_list):
    keywords_list = get_keywords('keywords.txt')
    result_data = []
    for keyword in keywords_list:
        if keyword not in msg_list:
            result_data.append(keyword)
    return result_data

def get_resou(keywords=[]):
    connection = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', db='test1',charset='utf8')
    cursor = connection.cursor()
    resou_str = ''
    for keyword in keywords:
        sql = "SELECT rank,keywords,flag,create_date FROM resou WHERE keywords like '%" + keyword + "%' ORDER BY rank ASC"
        cursor.execute(sql)
        resou_data = cursor.fetchall()
        for index,resou in enumerate(resou_data):
            tmp_date = str(resou[3])[str(resou[3]).find(' ') + 1:]
            tmp_str = tmp_date + ' ' + resou[1] + ' rank ' + str(resou[0]) +' '+ resou[2]
            resou_str += tmp_str + '\n'
    cursor.close()
    connection.close()
    return resou_str

def get_huati(keywords=[]):
    connection = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', db='test1',charset='utf8')
    cursor = connection.cursor()
    huati_str = ''
    for keyword in keywords:
        sql = "SELECT rank,name,create_date FROM huati WHERE name like '%" + keyword + "%' ORDER BY rank ASC"
        cursor.execute(sql)
        huati_data = cursor.fetchall()
        for huati in huati_data:
            tmp_date = str(huati[2])[str(huati[2]).find(' ') + 1:]
            tmp_str = tmp_date + ' ' + huati[1] + ' rank ' + str(huati[0])
            huati_str += tmp_str + '\n'
    cursor.close()
    connection.close()
    return huati_str

def main():
    bot = Bot(console_qr=False,cache_path=True)
    # 选择微信发送人
    #my_friend = bot.friends().search(u'婕婕')[0]
    #friends = []
    #friends.append(my_friend)
    friends = bot.friends()
    msg_list = get_keywords('keywords.txt')
    print json.dumps(msg_list, ensure_ascii=False, indent=4)
    print 'start send huati'
    huati_send(msg_list, friends)
    print 'start send resou'
    resou_send(msg_list, friends)
    t1 = threading.Thread(target=resou_send_ext, args=(friends,))
    t2 = threading.Thread(target=hauti_send_ext, args=(friends,))
    t1.start()
    t2.start()

def hauti_send_ext(friends):
    print 'huati send ext start! date-->',datetime.datetime.now()
    while True:
        # 确定到小时中的分钟数量
        minute = datetime.datetime.now().time().minute
        msg_list = get_keywords('keywords.txt')
        if minute == 36:
            print json.dumps(msg_list, ensure_ascii=False, indent=4)
            print 'start send huati'
            huati_send(msg_list, friends)
            print 'huati send ok! date now -->',datetime.datetime.now()
            time.sleep(60)
            print 'huati send start sleep. date --> 60s'
        time.sleep(10)
        print 'huati send start sleep. date --> 10s'

def resou_send_ext(friends):
    print 'resou send ext start! date-->',datetime.datetime.now()
    while True:
        sleep_time = random.randint(60 * 2, 60 * 3)
        print 'resou send start sleep. date -->'+str(sleep_time)+'s'
        time.sleep(sleep_time)
        msg_list = get_keywords('keywords.txt')
        print json.dumps(msg_list, ensure_ascii=False, indent=4)
        print 'start send resou'
        resou_send(msg_list,friends)
        print 'resou send ok! date now -->',datetime.datetime.now()

# 话题发送
def huati_send(msg_list,friends):
    huati_str = get_huati(msg_list)
    if huati_str:
        for my_friend in friends:
            try:
                my_friend.send_msg(huati_str)
                print my_friend, '-->ok'
                print huati_str
            except Exception,e:
                print e
                continue

# 热搜发送
def resou_send(msg_list,friends):
    resou_str = get_resou(msg_list)
    if resou_str:
        for my_friend in friends:
            try:
                my_friend.send_msg(resou_str)
                print my_friend, '-->ok'
                print resou_str
            except Exception,e:
                print e
                continue

if __name__ == '__main__':
   main()
   #print get_data('婆')