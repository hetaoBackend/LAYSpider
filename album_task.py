#!/usr/bin/python3
#-*- coding:utf-8 -*-
import requests
import json
import pymysql
import time
import datetime
import sched
from album_detail import getAlbumInfo, getAlbumExtra

# 插入salenum表
def insert_salenum(album_extra):
    db = pymysql.connect("localhost", "root", "12345678", "test", charset='utf8')
    cursor = db.cursor()
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = """
            INSERT INTO salenum(AlbID, AlbName, SalNum, CreateTime) \
            VALUES ({0}, "{1}", {2},"{3}" )"""\
                .format(album_extra['album_id'], album_extra['album_name'], album_extra['soldcount'],time_now )
    print(sql)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()

# salenum表更新任务
def task():
    album_meta = getAlbumInfo(album_mid)
    if 'id' in album_meta:
        album_id = album_meta['id']
        album_extra = getAlbumExtra(album_mid, album_id)
    #-------------------------------------------#
    # start salenum table
    print("--start inserting salenum table--")
    insert_salenum(album_extra)
    print("--finsh inserting salenum table--")
    #-------------------------------------------#

# 每个 3600 秒执行统计任务。
def timedTask():
    # 初始化 sched 模块的 scheduler 类
    scheduler = sched.scheduler(time.time, time.sleep)
    # 增加调度任务
    scheduler.enter(3600, 1, task)
    # 运行任务
    scheduler.run()

if __name__ == "__main__":
    # 从控制台输入album_url
    album_url = input("album_url:")
    album_mid = album_url.lstrip('https://y.qq.com/n/yqq/album/').rstrip('.html')
    #album_mid = "001T7G8z0o9FlF"  # album的url后缀
    if album_mid == "":
        print("illegal album_url, please check!")
        raise RuntimeError('illegal url')
    print('--the first insert start--')
    task()
    print('--the first insert end--')
    print('--the timetask start--')
    while 1:
        timedTask()
