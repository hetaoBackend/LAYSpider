#!/usr/bin/python
#-*- coding: UTF-8 -*-
#coding=utf-8
import re
import rsa
import time
import json
import base64
import logging
import binascii
import requests
import MySQLdb
import datetime
import urllib
import random
import traceback
import sys
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')

def get_proxy():
    # 这里填写无忧代理IP提供的API订单号（请到用户中心获取）
    order = "8c2d96b84bbd045a72bab2a02b5d969e"
    # 获取IP的API接口
    apiUrl = "http://api.ip.data5u.com/dynamic/get.html?order=" + order
    # 要抓取的目标网站地址
    targetUrl = "http://2017.ip138.com/ic.asp"
    targetUrl = "http://weibo.com"
    res = urllib.urlopen(apiUrl).read().strip("\n")
    session = requests.Session()
    print res
    print session.get(targetUrl,proxies={'http':'http://' + res}).content
    return res

class WeiBoLogin(object):
    """
    class of WeiBoLogin, to login weibo.com
    """

    def __init__(self):
        """
        constructor
        """
        self.user_name = None
        self.pass_word = None
        self.user_uniqueid = None
        self.user_nick = None
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0"})
        self.session.get("http://weibo.com/login.php")
        return

    def login(self, user_name, pass_word):
        """
        login weibo.com, return True or False
        """
        self.user_name = user_name
        self.pass_word = pass_word
        self.user_uniqueid = None
        self.user_nick = None

        # get json data
        s_user_name = self.get_username()
        json_data = self.get_json_data(su_value=s_user_name)
        if not json_data:
            return False
        s_pass_word = self.get_password(json_data["servertime"], json_data["nonce"], json_data["pubkey"])

        # make post_data
        post_data = {
            "entry": "weibo",
            "gateway": "1",
            "from": "",
            "savestate": "7",
            "userticket": "1",
            "vsnf": "1",
            "service": "miniblog",
            "encoding": "UTF-8",
            "pwencode": "rsa2",
            "sr": "1280*800",
            "prelt": "529",
            "url": "http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
            "rsakv": json_data["rsakv"],
            "servertime": json_data["servertime"],
            "nonce": json_data["nonce"],
            "su": s_user_name,
            "sp": s_pass_word,
            "returntype": "TEXT",
        }

        # get captcha code
        if json_data["showpin"] == 1:
            url = "http://login.sina.com.cn/cgi/pin.php?r=%d&s=0&p=%s" % (int(time.time()), json_data["pcid"])
            with open("captcha.jpeg", "wb") as file_out:
                file_out.write(self.session.get(url).content)
            code = raw_input("please enter your code:")
            post_data["pcid"] = json_data["pcid"]
            post_data["door"] = code

        # login weibo.com
        login_url_1 = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)&_=%d" % int(time.time())
        json_data_1 = self.session.post(login_url_1, data=post_data).json()
        if json_data_1["retcode"] == "0":
            params = {
                "callback": "sinaSSOController.callbackLoginStatus",
                "client": "ssologin.js(v1.4.18)",
                "ticket": json_data_1["ticket"],
                "ssosavestate": int(time.time()),
                "_": int(time.time()*1000),
            }
            response = self.session.get("https://passport.weibo.com/wbsso/login", params=params)
            json_data_2 = json.loads(re.search(r"\((?P<result>.*)\)", response.text).group("result"))
            if json_data_2["result"] is True:
                self.user_uniqueid = json_data_2["userinfo"]["uniqueid"]
                self.user_nick = json_data_2["userinfo"]["displayname"]
                cookies_dict = requests.utils.dict_from_cookiejar(self.session.cookies)
                open('6666.txt','w').write(str(cookies_dict))
                print json.dumps(json_data_2,ensure_ascii=False,indent=4)
                logging.warning("WeiBoLogin succeed: %s", json_data_2)
            else:
                logging.warning("WeiBoLogin failed: %s", json_data_2)
        else:
            print json.dumps(json_data_1,ensure_ascii=False,indent=4)
            logging.warning("WeiBoLogin failed: %s", json_data_1)
        return True if self.user_uniqueid and self.user_nick else False

    def get_username(self):
        """
        get legal username
        """
        username_quote = urllib.quote_plus(self.user_name)
        username_base64 = base64.b64encode(username_quote.encode("utf-8"))
        return username_base64.decode("utf-8")

    def get_json_data(self, su_value):
        """
        get the value of "servertime", "nonce", "pubkey", "rsakv" and "showpin", etc
        """
        params = {
            "entry": "weibo",
            "callback": "sinaSSOController.preloginCallBack",
            "rsakt": "mod",
            "checkpin": "1",
            "client": "ssologin.js(v1.4.18)",
            "su": su_value,
            "_": int(time.time()*1000),
        }
        try:
            response = self.session.get("http://login.sina.com.cn/sso/prelogin.php", params=params)
            json_data = json.loads(re.search(r"\((?P<data>.*)\)", response.text).group("data"))
        except Exception as excep:
            json_data = {}
            logging.error("WeiBoLogin get_json_data error: %s", excep)

        logging.debug("WeiBoLogin get_json_data: %s", json_data)
        return json_data

    def get_password(self, servertime, nonce, pubkey):
        """
        get legal password
        """
        string = (str(servertime) + "\t" + str(nonce) + "\n" + str(self.pass_word)).encode("utf-8")
        public_key = rsa.PublicKey(int(pubkey, 16), int("10001", 16))
        password = rsa.encrypt(string, public_key)
        password = binascii.b2a_hex(password)
        return password.decode()

def insert_data(dict_arr):
    connection = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', db='test',charset='utf8')
    cursor = connection.cursor()
    # 删除数据
    sql = "DELETE FROM huati "
    cursor.execute(sql)
    connection.commit()
    print 'delete huati table ok -->', datetime.datetime.now()
    for dict_data in dict_arr:
        name = dict_data['name']
        rank = dict_data['rank']
        sql = "INSERT INTO huati VALUES (DEFAULT ,'"+rank+"','"+name+"','',NOW(),NOW())"
        cursor.execute(sql)
        connection.commit()
        sql = "INSERT INTO huati_history VALUES (DEFAULT ,'"+rank+"','"+name+"','',NOW(),NOW())"
        cursor.execute(sql)
        connection.commit()
    print 'huati insert into data ok! -->', (datetime.datetime.now())
    cursor.close()
    connection.close()

def get_data_info():
    flag = True
    i = 0
    while flag:
        flag = False
        try:
            session = requests.Session()
            cookie_data = open('6666.txt', 'r').read()
            cookie_json = json.loads(cookie_data.replace("'", '"'))
            session.headers.update(
                {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0"})
            session.cookies = requests.utils.cookiejar_from_dict(cookie_json)
            dict_data_arr = []
            for page_index in xrange(1, 6):
                content = ''
                try:
                    #url = 'https://d.weibo.com/100803?cfs=920&Pl_Discover_Pt6Rank__5_filter=&Pl_Discover_Pt6Rank__5_page='+str(page_index)+' #Pl_Discover_Pt6Rank__5'
                    url = 'https://d.weibo.com/100803?pids=Pl_Discover_Pt6Rank__5&cfs=920&Pl_Discover_Pt6Rank__5_filter=&Pl_Discover_Pt6Rank__5_page=' + str(page_index) + '&ajaxpagelet=1'
                   
                    rsp = session.get(url)
                    content = rsp.content
                    content = re.findall('{.+}', rsp.content)[0]
                    #print content
                    # content = open('11.html','r').read()
                    json_data = json.loads(content)
                    content_html = json_data['html']
                    content_html = content_html.replace('\r', '').replace('\n', '').replace('\t', '')
                    soup = BeautifulSoup(content_html, 'lxml')
                    ul = soup.find_all('ul')[1]
                    for li in ul.find_all('li'):
                        dict_data = {}
                        top = li.find('div').find('span').string
                        # top = li.find('div').find('div').find('a').find('span').contents
                        if top.find(u'推荐') == 0:
                            continue
                        rank = re.findall('\d+', top)[0]
                        dict_data['rank'] = rank
                        name = li.find('div').find('div').find('img').get('alt')
                        dict_data["name"] = name
                        dict_data_arr.append(dict_data)
                except Exception,e:
                    open(str(datetime.datetime.now()).replace(':','').replace('-','').replace(' ','').replace('.','')+'.log','w').write(content)
                    print e
                    traceback.print_exc()
                    continue
            # 插入数据
            insert_data(dict_data_arr)
        except Exception,e:
            traceback.print_exc()
            flag = True
            i += 1
        if i > 10:
            print 'error please manager'
            time.sleep(2)

if __name__ == "__main__":
    #get_proxy()
    weibo = WeiBoLogin()
    user_name = '2287020580@qq.com'
    pwd = '930909lzj'
    #weibo.get_data()
    print 'start up -->',datetime.datetime.now()
    weibo.login(user_name, pwd)
    # 爬虫
    get_data_info()
    while True:
        # 确定到小时中的分钟数量
        minute = datetime.datetime.now().time().minute
        if minute == 35:
            # 爬虫
            
            weibo.login(user_name, pwd)
            get_data_info()
            time.sleep(60)
        time.sleep(10)