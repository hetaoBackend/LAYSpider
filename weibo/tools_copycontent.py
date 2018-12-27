#!/usr/bin/python
#-*- coding: UTF-8 -*-
#coding=utf-8
import os
import re
import requests
import sys
import traceback
import json
import urllib
import MySQLdb
from bs4 import BeautifulSoup
import random
import datetime
from lxml import etree
from ThreadPool import *
import time
reload(sys)
sys.setdefaultencoding("utf-8")
requests.packages.urllib3.disable_warnings()

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
REQUEST_TIME_OUT = 5
# 最大子线程数量
MAX_THREAD = 20
# 主页信息 3655689037
WEIBO_MAIN_URL = "https://m.weibo.cn/u/1976287937?uid=1976287937&display=0&retcode=6102"

# 用户主页个人信息
WEIBO_USER_URL = "https://m.weibo.cn/api/container/getIndex?display=0&retcode=6102&type=uid&value=1976287937"

# 爬虫微博链接
WEIBO_LINK_URL = "https://m.weibo.cn/api/container/getIndex?display=0&retcode=6102&containerid=1076031976287937&page=0"

# 留言API
URL_COMMIT_URL = "https://m.weibo.cn/api/comments/show?id=4184562986557218&page=1"

# 微博内容信息
WEIBO_CONET_URL = "http://m.weibo.cn/status/4184562986557218?display=0&retcode=6102"

from DBUtils.PooledDB import PooledDB
pool = PooledDB(MySQLdb,20,host='127.0.0.1',user='root',passwd='root',db='weibo',port=3306,charset='utf8')
#connection = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', db='weibo',charset='utf8')
#cursor = connection.cursor()
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
        'Cookie':'YF-V5-G0=c072c6ac12a0526ff9af4f0716396363; SUB=_2AkMtGthpf8NxqwJRmPERym3gaY52yQ3EieKbRimyJRMxHRl-yT83qlIftRB6Bpr2hlUGh32nmRR_8vc9I8Rgwp1bCWk-; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFCRjMNjhb2x9ghA7TZ-1Ce'
    }
    #county = get_countiy(url)
    #ip_proexy = get_random_proxy(county)
    #返回内容
    result_text = '请求错误'
    try:
        if 'get' in method:
           # rs = requests.get(url, data=data, headers=HEADER, timeout=REQUEST_TIME_OUT,proxies=ip_proexy)
            rs = requests.get(url, data=data, headers=HEADER, timeout=REQUEST_TIME_OUT,verify=False)
            print url
            print 'code ----------',rs.status_code
            if rs.status_code == 200:
                result_text = rs.text
            else:
                while True:
                    print 'url ',url
                    print 'start sleep ',60
                    time.sleep(60)
                    rs = requests.get(url, data=data, headers=HEADER, timeout=REQUEST_TIME_OUT,verify=False)
                    if rs.status_code == 200:
                        result_text = rs.text
                        break
        elif 'post' in method:
            #rs = requests.post(url, data=data, headers=HEADER, timeout=REQUEST_TIME_OUT,proxies=ip_proexy)
            rs = requests.get(url, data=data, headers=HEADER, timeout=REQUEST_TIME_OUT,verify=False)
            if rs.status_code == 200:
                result_text = rs.text
    except Exception, e:
        pass
    return result_text

"""
读取微博用户信息
"""
def get_user_info(user_id):
    url = WEIBO_USER_URL.replace('value=1976287937','value='+user_id)
    rs = requests.get(url,verify=False)
    result_data = ''
    result_data = request_url(url,'get','')
    if '用户不存在' in result_data:
        return
    result_json = json.loads(result_data)
    flag = result_json["ok"]
    # 提取成功数据
    if flag == 1:
        #print json.dumps(result_json,ensure_ascii=False)
        user_info_dict = {}
        user_info_json = {}
        tabs_info = {}
        if result_json.has_key('data'):
            user_info_dict = result_json["data"]["userInfo"]
            tabs_info = result_json["data"]["tabsInfo"]
        else:
            user_info_dict = result_json["userInfo"]
            tabs_info = result_json["tabsInfo"]
        tabs = tabs_info['tabs']
        for tab in tabs:
            if tab['tab_type'] == 'profile':
                user_info_json['profile_container_id'] = tab['containerid']
            elif tab['tab_type'] == 'weibo':
                user_info_json['weibo_container_id'] = tab['containerid']
        user_info_json['user_id'] = user_id
        user_info_json['screen_name'] = user_info_dict['screen_name']
        user_info_json['followers_count'] = user_info_dict['followers_count']
        user_info_json['follow_count'] = user_info_dict['follow_count']
        user_info_json['profile_image_url'] = user_info_dict['profile_image_url']
        user_info_json['profile_url'] = user_info_dict['profile_url']
        user_info_json['statuses_count'] = user_info_dict['statuses_count']
        user_info_json['description'] = user_info_dict['description']
        user_info_json['verified_reason'] = user_info_dict['verified_reason']
        #print json.dumps(user_info_json,ensure_ascii=False,indent=4)
        insert_user_info_data(user_info_json)

"""
插入用户数据
"""
def insert_user_info_data(user_info_json):
    user_id = str(user_info_json['user_id'])
    user_id = MySQLdb.escape_string(user_id)
    screen_name = str(user_info_json['screen_name'])
    screen_name = MySQLdb.escape_string(screen_name)
    followers_count = str(user_info_json['followers_count'])
    followers_count = MySQLdb.escape_string(followers_count)
    follow_count = str(user_info_json['follow_count'])
    follow_count = MySQLdb.escape_string(follow_count)
    profile_image_url = str(user_info_json['profile_image_url'])
    profile_image_url = MySQLdb.escape_string(profile_image_url)
    profile_url = str(user_info_json['profile_url'])
    profile_url = MySQLdb.escape_string(profile_url)
    statuses_count = str(user_info_json['statuses_count'])
    statuses_count = MySQLdb.escape_string(statuses_count)
    description = str(user_info_json['description'])
    description = MySQLdb.escape_string(description)
    verified_reason = str(user_info_json['verified_reason'])
    verified_reason = MySQLdb.escape_string(verified_reason)
    weibo_container_id = str(user_info_json['weibo_container_id'])
    weibo_container_id = MySQLdb.escape_string(weibo_container_id)
    profile_container_id = str(user_info_json['profile_container_id'])
    profile_container_id = MySQLdb.escape_string(profile_container_id)
    # 检索是否存在数据,如果存在删除原有数据
    exist_user_info(user_id)
    sql = "INSERT INTO weibo_user (id,user_id,screen_name,followers_count,follow_count,profile_image_url,profile_url,statuses_count,description,verified_reason,create_date,update_date,weibo_container_id,profile_container_id) VALUES(DEFAULT,'"+user_id+"','"+screen_name+"','"+followers_count+"','"+follow_count+"','"+profile_image_url+"','"+profile_url+"','"+statuses_count+"','"+description+"','"+verified_reason+"',NOW(),NOW(),'"+weibo_container_id+"','"+profile_container_id+"')"
    #connection = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', db='weibo',charset='utf8')
    connection = pool.connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()
    print 'weibo user info -->ok'
    print json.dumps(user_info_json,ensure_ascii=False,indent=4)

"""
检索用户数据是否存在
"""
def exist_user_info(user_id):
    #connection = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', db='weibo',charset='utf8')
    connection = pool.connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM weibo_user WHERE user_id = '"+user_id+"'"
    cursor.execute(sql)
    data = cursor.fetchall()
    if len(data) > 0:
        sql = "DELETE FROM weibo_user WHERE user_id = '"+user_id+"'"
        cursor.execute(sql)
        connection.commit()
    cursor.close()
    connection.close()

"""
读取containerid
"""
def get_containerid(user_id):
    container_id = ''
    #connection = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', db='weibo',charset='utf8')
    connection = pool.connection()
    cursor = connection.cursor()
    sql = "SELECT weibo_container_id FROM weibo_user WHERE user_id = '"+user_id+"'"
    cursor.execute(sql)
    data = cursor.fetchone()
    if data:
        container_id = data[0]
    cursor.close()
    connection.close()
    return container_id

"""
读取微博的ID
"""
def get_weibo_link(user_id,container_id,start_date,end_date):
    print 'loading weibo link ....'
    url = WEIBO_LINK_URL.replace('value=1976287937','value='+user_id).replace('uid=1976287937','uid='+user_id).replace('containerid=1076031976287937','containerid='+container_id)
    #url = WEIBO_LINK_URL
    content = request_url(url,'get','')
    result_json = json.loads(content)
    flag = result_json["ok"]
    page_count = 0
    total = 0
    cards = []
    if result_json.has_key('data'):
        # 计算页数
        data = result_json["data"]
        total = data['cardlistInfo']['total']
        cards = data['cards']
    else:
        total = result_json['cardlistInfo']['total']
        cards = result_json['cards']
    if total % 10 == 0:
        page_count = total / 10
    else:
        page_count = total / 10 + 1
    i = datetime.datetime.now()
    # 当前时间
    hour = i.hour
    # 当前年份
    year = i.year
    # 当前月份
    month = i.month
    # 当前天数
    day = i.day
    # 微博ID字典
    weibo_dict = {}
    for card in cards:
        try:
            id = card['mblog']['id']
            created_at = card['mblog']['created_at']
            if '小时' in created_at:
                created_at = created_at.replace('小时前','')
                if hour >= int(created_at):
                    date_now = str(year)+'-'+str(month)+'-'+str(day)
                    created_at = date_now
                else:
                    date_now = str(year)+'-'+str(month)+'-'+str(day)
                    created_at = date_now
            elif '分钟' in created_at:
                date_now = str(year)+'-'+str(month)+'-'+str(day)
                created_at = date_now
            elif '昨天' in created_at:
                date_now = str(year)+'-'+str(month)+'-'+str(day-1)
                created_at = date_now
            elif created_at.count('-') == 1:
                    created_at = str(year) + '-'+created_at
            created_at_time = datetime.datetime.strptime(created_at, '%Y-%m-%d')
            print id,created_at_time
            if created_at_time < start_date:
                print '---------------------------'
                print '< ',id,created_at
                print '---------------------------'
                continue
            if created_at_time > end_date:
                print '---------------------------'
                print '> ',id,created_at
                print '---------------------------'
                continue
            if weibo_dict.has_key(id):
                print '---------------------------'
                print 'has ',id,created_at
                print '---------------------------'
                continue
            print id,created_at,'--->pass'
            weibo_dict[id] = created_at
        except Exception as e:
            print e
            continue
    #print json.dumps(weibo_dict,ensure_ascii=False)
    for index in range(1,page_count+1):
        url = url.replace('&page='+str(index-1),'&page='+str(index))
        content = request_url(url,'get','')
        result_json = json.loads(content)
        flag = result_json["ok"]
        cards = []
        if result_json.has_key('data'):
            data = result_json["data"]
            cards = data['cards']
        else:
            cards = result_json['cards']
        print 'page lenth -->',len(cards)
        error_count = 0
        for card in cards:
            try:
                id = card['mblog']['id']
                created_at = card['mblog']['created_at']
                if '小时' in created_at:
                    created_at = created_at.replace('小时前','')
                    if hour >= int(created_at):
                        date_now = str(year)+'-'+str(month)+'-'+str(day)
                        created_at = date_now
                    else:
                        date_now = str(year)+'-'+str(month)+'-'+str(day)
                        created_at = date_now
                elif '分钟' in created_at:
                    date_now = str(year)+'-'+str(month)+'-'+str(day)
                    created_at = date_now
                elif '昨天' in created_at:
                    date_now = str(year)+'-'+str(month)+'-'+str(day-1)
                    created_at = date_now
                elif created_at.count('-') == 1:
                    created_at = str(year) + '-'+created_at
                created_at_time = datetime.datetime.strptime(created_at, '%Y-%m-%d')
                print id,created_at
                if created_at_time < start_date:
                    print '---------------------------'
                    print '< ',id,created_at
                    print '---------------------------'
                    continue
                if created_at_time > end_date:
                    print '---------------------------'
                    print '> ',id,created_at
                    print '---------------------------'
                    continue
                if weibo_dict.has_key(id):
                    print '---------------------------'
                    print 'has ',id,created_at
                    print '---------------------------'
                    continue
                print id,created_at,'--->pass'
                weibo_dict[id] = created_at
                if error_count >= 2:
                    break
            except Exception as e:
                print e
                continue
    return weibo_dict

"""
解析微博内容
"""
def get_weibo_content(user_id,weibo_content_id,created_at):
    url = WEIBO_CONET_URL.replace('/4184562986557218','/'+weibo_content_id)
    content = request_url(url,'get','')
    if '出错了' in content:
        return
    content = content.replace(' ','').replace('\n','').replace('\t','')
    render_data_index = content.find('render_data=')
    test_str = content[render_data_index:]
    #print test_str
    sc_index = test_str.find('[0]||{};</script>')
    test_str = test_str[:sc_index].replace('render_data=','')
    try:
        result_json_arr = json.loads(test_str)
        if len(result_json_arr) > 0:
            result_json = result_json_arr[0]
            status_json = result_json['status']
            text = status_json['text']
            soup = BeautifulSoup(text,'lxml')
            text = soup.text
            # 分享数量
            reposts_count = status_json['reposts_count']
            # 留言数量
            comments_count = status_json['comments_count']
            # 点赞数量
            attitudes_count = status_json['attitudes_count']
            weibo_content_json = {
                'text':text,
                'reposts_count':reposts_count,
                'comments_count':comments_count,
                'attitudes_count':attitudes_count,
                'weibo_content_id':weibo_content_id,
                'user_id':user_id,
                'created_at':created_at
            }
            insert_weibo_content(weibo_content_json)
    except Exception as e:
        pass

"""
插入微博留言内容数据
"""
def insert_weibo_comment(comment_json_arr):
    #connection = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', db='weibo',charset='utf8')
    #cursor = connection.cursor()
    connection = pool.connection()
    cursor = connection.cursor()
    values = []
    comment_ids = []
    for comment_json in comment_json_arr:
        text = str(comment_json['text'])
        text = MySQLdb.escape_string(text)
        id = str(comment_json['id'])
        id = MySQLdb.escape_string(id)
        user_id = str(comment_json['user_id'])
        user_id = MySQLdb.escape_string(user_id)
        created_at = str(comment_json['created_at'])
        created_at = MySQLdb.escape_string(created_at)
        comment_user_id = str(comment_json['comment_user_id'])
        comment_user_id = MySQLdb.escape_string(comment_user_id)
        user_id = str(comment_json['user_id'])
        user_id = MySQLdb.escape_string(user_id)
        screen_name = str(comment_json['screen_name'])
        screen_name = MySQLdb.escape_string(screen_name)
        profile_url = str(comment_json['profile_url'])
        profile_url = MySQLdb.escape_string(profile_url)
        weibo_content_id = str(comment_json['weibo_content_id'])
        weibo_content_id = MySQLdb.escape_string(weibo_content_id)
        #sql = "DELETE FROM weibo_comment WHERE comment_id = " + id
        #cursor.execute(sql)
        #connection.commit()
        values.append((weibo_content_id,user_id,screen_name,profile_url,id,text,comment_user_id,created_at))
        comment_ids.append(id)
        #sql = "INSERT INTO weibo_comment(id,weibo_content_id,user_id,screen_name,profile_url,comment_id,text,comment_user_id,created_at,create_date,update_date) VALUES(DEFAULT,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())"
        #sql = "INSERT INTO weibo_comment(id,weibo_content_id,user_id,screen_name,profile_url,comment_id,text,comment_user_id,created_at,create_date,update_date) VALUES(DEFAULT,'"+weibo_content_id+"','"+user_id+"','"+screen_name+"','"+profile_url+"','"+id+"','"+text+"','"+comment_user_id+"','"+created_at+"',NOW(),NOW())"
        #cursor.execute(sql)
        #connection.commit()
        
    # sql = "INSERT INTO weibo_comment(id,weibo_content_id,user_id,screen_name,profile_url,comment_id,text,comment_user_id,created_at,create_date,update_date) VALUES(DEFAULT,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())"
    try:
        sql = " INSERT IGNORE INTO weibo_comment(id,weibo_content_id,user_id,screen_name,profile_url,comment_id,text,comment_user_id,created_at,create_date,update_date) VALUES(DEFAULT,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())"
        cursor.executemany(sql,values)
        print 'ID:',comment_ids,' comment -->ok'
        connection.commit()
    except Exception as e:
        print e
        raise e
    #print json.dumps(values,ensure_ascii=False,indent=4)
    cursor.close()
    connection.close()
    #print json.dumps(comment_json,ensure_ascii=False,indent=4)

"""
插入微博内容数据
"""
def insert_weibo_content(weibo_content_json):
    user_id = str(weibo_content_json['user_id'])
    user_id = MySQLdb.escape_string(user_id)
    weibo_content_id = str(weibo_content_json['weibo_content_id'])
    weibo_content_id = MySQLdb.escape_string(weibo_content_id)
    text = str(weibo_content_json['text'])
    text = MySQLdb.escape_string(text)
    reposts_count = str(weibo_content_json['reposts_count'])
    reposts_count = MySQLdb.escape_string(reposts_count)
    comments_count = str(weibo_content_json['comments_count'])
    comments_count = MySQLdb.escape_string(comments_count)
    attitudes_count = str(weibo_content_json['attitudes_count'])
    attitudes_count = MySQLdb.escape_string(attitudes_count)
    created_at = str(weibo_content_json['created_at'])
    created_at = MySQLdb.escape_string(created_at)
    #connection = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', db='weibo',charset='utf8')
    connection = pool.connection()
    cursor = connection.cursor()
    #sql = "DELETE FROM weibo_content WHERE weibo_content_id = "+weibo_content_id
    #cursor.execute(sql)
    #connection.commit()
    sql = "INSERT IGNORE INTO weibo_content(id,user_id,weibo_content_id,text,reposts_count,comments_count,attitudes_count,created_at,create_date,update_date) VALUES(DEFAULT,'"+user_id+"','"+weibo_content_id+"','"+text+"','"+reposts_count+"','"+comments_count+"','"+attitudes_count+"','"+created_at+"',NOW(),NOW())"
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()
    print 'ID:'+weibo_content_id+' weibo content -->ok'
    #print json.dumps(weibo_content_json,ensure_ascii=False,indent=4)

"""
微博内容采集函数
"""
def siper_weibo_content(weibo_link_dict):
    content_pool = ThreadPool(MAX_THREAD)
    print 'this weibo total -->',len(weibo_link_dict)
    print 'weibo content siper start ....'
    # 采集微博内容信息
    for weibo_content_id in weibo_link_dict:
        created_at = weibo_link_dict[weibo_content_id]
        content_pool.run(get_weibo_content, (user_id,weibo_content_id,created_at), callback=None)
        # 采集微博内容信息
        #get_weibo_content(user_id,weibo_content_id,created_at)
    print 'weibo content siper end ....'
    content_pool.close()

"""
微博评论采集
"""
def siper_weibo_comment(weibo_link_dict,user_id):
    comment_pool = ThreadPool(MAX_THREAD)
    print 'weibo comment siper start ...'
    for weibo_content_id in weibo_link_dict:
        created_at = weibo_link_dict[weibo_content_id]
        print weibo_content_id,created_at
        #get_weibo_comment_spider(weibo_content_id,user_id)
        comment_pool.run(get_weibo_comment_spider, (weibo_content_id,user_id,), callback=None)
        # 解析微博评论
        #get_weibo_comment(weibo_content_id)
    print 'weibo comment siper end ...'
    comment_pool.close()

"""
主函数
"""
def siper_data(user_id,start_date,end_date):
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    # 采集微博用户信息
    get_user_info(user_id)
    main_pool = ThreadPool(MAX_THREAD)
    # 读取微博ID
    container_id = get_containerid(user_id)
    # 采集微博LINK时间以及ID
    weibo_link_dict = get_weibo_link(user_id,container_id,start_date,end_date)
    main_pool.run(siper_weibo_content,(weibo_link_dict,), callback=None)
    #main_pool.run(siper_weibo_comment,(weibo_link_dict,user_id,), callback=None)
    main_pool.close()

"""
提取微博留言扩展版本
"""
def get_weibo_comment_ext(url,content_id,user_id):
    #url = 'https://weibo.com/aj/v6/comment/big?id=4183891046515457&filter=all&page=1'
    except_flag = True
    content_json = {}
    while except_flag:
        try:
            content = request_url(url,'get','')
            content_json = json.loads(content)
            except_flag = False
        except Exception as e:
            except_flag = True
    html = content_json['data']['html']
    page_count = content_json['data']['page']['totalpage']
    soup = BeautifulSoup(html,'lxml')
    #print soup
    li_arr = soup.find_all('div',class_='S_line1')
    #insert_weibo_comment_pool = ThreadPool(5)
    test_arr = []
    for li in li_arr:
        if not li.has_attr("comment_id"):
            continue
        comment_id = li.attrs["comment_id"]
        comment_user_id = ''
        user_main_url = ''
        a_arr = li.find('div',class_='WB_text').find_all('a')
        for a in a_arr:
            if a.has_attr("usercard"):
                comment_user_id = a.attrs['usercard'].replace('id=','')
                user_main_url = a.attrs['href']
                break
        screen_name = li.find('div',class_='WB_text').find('a').string
        comment_content = li.find('div',class_='WB_text').text
        comment_content = comment_content.replace(screen_name+'：','').replace(screen_name+':','')
        comment_content = comment_content.replace('\n','')
        now_date = datetime.datetime.now()
        # 当前时间
        hour = now_date.hour
        # 当前年份
        year = now_date.year
        # 当前月份
        month = now_date.month
        # 当前天数
        day = now_date.day
        created_at = ''
        date = li.find('div',class_='S_txt2').string
        if '秒' in date:
            tmp_int = int(date.replace('秒前','').replace(' ',''))
            now_date = now_date - datetime.timedelta(seconds=tmp_int)
            created_at = now_date.strftime('%Y-%m-%d %H:%M')
        elif '分钟' in date:
            tmp_int = int(date.replace('分钟前','').replace(' ',''))
            now_date = now_date - datetime.timedelta(minutes=tmp_int)
            created_at = now_date.strftime('%Y-%m-%d %H:%M')
        elif '小时' in date:
            tmp_int = int(date.replace('小时前','').replace(' ',''))
            now_date = now_date - datetime.timedelta(hours=tmp_int)
            created_at = now_date.strftime('%Y-%m-%d %H:%M')
        elif '今天' in date:
            date = date.replace(' ','').replace('今天',' ')
            now_date = str(year) + '-'+str(month)+'-'+str(day)+date
            now_date = datetime.datetime.strptime(now_date, '%Y-%m-%d %H:%M')
            created_at = now_date.strftime('%Y-%m-%d %H:%M')
        elif '昨天' in date:
            date = date.replace(' ','').replace('昨天',' ')
            now_date = str(year) + '-'+str(month)+'-'+str(day-1)+date
            now_date = datetime.datetime.strptime(now_date, '%Y-%m-%d %H:%M')
            created_at = now_date.strftime('%Y-%m-%d %H:%M')
        elif '天前' in date:
            tmp_int = int(date.replace('天前','').replace(' ',''))
            now_date = now_date - datetime.timedelta(days=tmp_int) 
            created_at = now_date.strftime('%Y-%m-%d %H:%M')
        else:
            if date.count('-') == 1:
                date = date.replace(' ','')
                date = date.replace('年','-').replace('月','-').replace('日',' ')
                now_date = str(year) + '-'+ date
                now_date = datetime.datetime.strptime(now_date, '%Y-%m-%d %H:%M')
                created_at = now_date.strftime('%Y-%m-%d %H:%M')
            elif date.count('-') == 2:
                tmp_date_arr = re.findall('\d \d{3}',date)
                for tmp_date in tmp_date_arr:
                    tmp_date_date = tmp_date.replace(' ','')
                    date = date.replace(tmp_date,tmp_date_date)
                created_at = date
            else:
                if '年' in date and '月' in date:
                    date = date.replace(' ','')
                    date = date.replace('年','-').replace('月','-').replace('日',' ')
                    now_date = date
                    now_date = datetime.datetime.strptime(now_date, '%Y-%m-%d %H:%M')
                    created_at = now_date.strftime('%Y-%m-%d %H:%M')
                elif '月' in date and '日' in date:
                    date = date.replace(' ','')
                    date = date.replace('月','-').replace('日',' ')
                    now_date = str(year) + '-'+ date
                    now_date = datetime.datetime.strptime(now_date, '%Y-%m-%d %H:%M')
                    created_at = now_date.strftime('%Y-%m-%d %H:%M')
            #now_date = datetime.datetime.strptime(now_date, '%Y-%m-%d %H:%M')
        #created_at = now_date.strftime('%Y-%m-%d %H:%M')
        comment_json = {
            'id':comment_id,
            'text':comment_content,
            'created_at':created_at,
            'user_id':user_id,
            'screen_name':screen_name,
            'profile_url':user_main_url,
            'weibo_content_id':content_id,
            'comment_user_id':comment_user_id,
        }
        test_arr.append(comment_json)
        '''try:
            # insert_weibo_comment(comment_json)
            insert_weibo_comment_pool.run(insert_weibo_comment, (comment_json,), callback=None)
        except Exception as e:
            print e
            continue'''
    #insert_weibo_comment_pool.close()
    if len(test_arr) > 0:
        insert_weibo_comment(test_arr)
    return page_count

"""
微博留言爬虫
"""
def get_weibo_comment_spider(content_id,user_id):
    url = 'https://weibo.com/aj/v6/comment/big?id='+content_id+'&filter=all&page=1'
    try:
        page_count = get_weibo_comment_ext(url,content_id,user_id)
        comment_pool = ThreadPool(MAX_THREAD)
        for i in range(2,page_count+1):
            url = 'https://weibo.com/aj/v6/comment/big?id='+content_id+'&filter=all&page='+str(i)
            try:
                #get_weibo_comment_ext(url,content_id,user_id)
                comment_pool.run(get_weibo_comment_ext, (url,content_id,user_id), callback=None)
            except Exception as e1:
                print e1
                traceback.print_exc()
                continue
        comment_pool.close()
    except Exception as e:
        traceback.print_exc()

if __name__ == '__main__':
    #user_id = '2706896955'
    #start_date = '2017-01-01'
    #end_date = '2018-12-31'
    user_id = '2706896955'
    start_date = '2018-01-01'
    end_date = '2018-06-30'
    try:
        #get_weibo_comment_ext()
        #get_weibo_comment_spider('4099477293933897','123')
        siper_data(user_id,start_date,end_date)
    except Exception as e:
        print e
        traceback.print_exc()
