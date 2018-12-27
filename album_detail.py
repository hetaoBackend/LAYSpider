#!/usr/bin/python3
#-*- coding:utf-8 -*-
import requests
import json
import pymysql

db = pymysql.connect("localhost", "root", "12345678", "test", charset='utf8')

# 获取专辑id和封面信息
def getAlbumInfo(album_mid):
    url = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_album_info_cp.fcg'
    header = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'referer':'https://y.qq.com/n/yqq/album/{}.html'.format(album_mid)
    }
    paramters = {
        'albummid':album_mid, #传入album_mid
        'g_tk':'5381',
        'jsonpCallback':'jsonp1',
        'loginUin':'0',
        'hostUin':'0',
        'format':'json',
        'inCharset':'utf8',
        'outCharset':'utf-8',
        'notice':'0',
        'platform':'yqq.json',
        'needNewCode':'0'
    }

    html = requests.get(url=url,params=paramters,headers=header)
    res = json.loads(html.text.strip().lstrip('jsonp1(').rstrip(')'))
    if 'data' in res:
        return res['data']
    else:
        return {}

# 获取专辑额外信息
def getAlbumExtra(album_mid, album_id):
    url = 'https://c.y.qq.com/v8/fcg-bin/musicmall.fcg'
    header = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'referer':'https://y.qq.com/n/yqq/album/{}.html'.format(album_mid)
    }
    paramters = {
        'cmd':'get_album_buy_page',
        'g_tk':'5381',
        'p':'0.8575604667634174',
        'albumid':album_id, #传入album_id
        'jsonpCallback':'jsonp1',
        'loginUin':'0',
        'hostUin':'0',
        'format':'json',
        'inCharset':'utf8',
        'outCharset':'utf-8',
        'notice':'0',
        'platform':'yqq.json',
        'needNewCode':'0'
    }

    html = requests.get(url=url,params=paramters,headers=header)
    res = json.loads(html.text.strip().lstrip('jsonp1(').rstrip(')'))
    if 'data' in res:
        return res['data']
    else:
        return {}

# 获得actid，用于获得用户贡献列表
def getActURL(album_mid, album_id):
    url = 'https://c.y.qq.com/shop/fcgi-bin/fcg_album_get_acturl'
    header = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'referer':'https://y.qq.com/n/yqq/album/{}.html'.format(album_mid)
    }
    paramters = {
        'g_tk':'5381',
        'p':'0.5363453918419474',
        'albumid':album_id, #传入album_id
        'jsonpCallback':'jsonp1',
        'loginUin':'0',
        'hostUin':'0',
        'format':'json',
        'inCharset':'utf8',
        'outCharset':'utf-8',
        'notice':'0',
        'platform':'yqq.json',
        'needNewCode':'0'
    }

    html = requests.get(url=url,params=paramters,headers=header)
    res = json.loads(html.text.strip().lstrip('jsonp1(').rstrip(')'))
    if 'data' in res:
        return res['data']
    else:
        return {}

# 获得用户排行榜，通过begin、end来进行分页，一页25个
def getAlbumRank(album_mid, actid, begin, end):
    url = 'https://c.y.qq.com/shop/fcgi-bin/fcg_album_rank'
    header = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'referer':'https://y.qq.com/n/yqq/album/{}.html'.format(album_mid)
    }
    rankname = "uin_rank_peract_{0}|uin_rank_peract_{0}_day".format(actid)
    paramters = {
        'begin':'{}'.format(begin),
        'end':'{}'.format(end),
        'rankname':rankname,
        'g_tk':'5381',
        'p':'0.8575604667634174',
        'jsonpCallback':'jsonp1',
        'loginUin':'0',
        'hostUin':'0',
        'format':'json',
        'inCharset':'utf8',
        'outCharset':'utf-8',
        'notice':'0',
        'platform':'yqq.json',
        'needNewCode':'0'
    }

    html = requests.get(url=url,params=paramters,headers=header)
    res = json.loads(html.text.strip().lstrip('jsonp1(').rstrip(')'))
    if 'data' in res:
        return res['data']
    else:
        return {}

# 获取评论列表信息
def getCommentInfo(source, album_mid, top_id, pagenum, lasthotcommentid):
    url = 'https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg'
    header = {
        'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'referer':'https://y.qq.com/n/yqq/{0}/{1}.html'.format(source, album_mid)
    }
    if source == "song":
        biztype = '1'
    elif source == "album":
        biztype = '2'
    paramters = {
        'g_tk':'5381',
        'topid':'{}'.format(top_id), #传入top_id
        'cmd':'8',
        'cid':'205360772',
        'reqtype':'2',
        'jsonpCallback':'jsonp1',
        'biztype':biztype,
        'domain':'qq.com',
        'ct':'24',
        'cv':'101010',
        'loginUin':'0',
        'hostUin':'0',
        'format':'json',
        'inCharset':'utf8',
        'outCharset':'GB2312',
        'needmusiccrit':'0',
        'pagenum':'{}'.format(pagenum),
        'pagesize':'25',
        'notice':'0',
        'platform':'yqq.json',
        'lasthotcommentid':lasthotcommentid,
        'needNewCode':'0'
    }
    html = requests.get(url=url,params=paramters,headers=header)
    res = json.loads(html.text.strip())
    return res

# 插入album表
def insert_album(album_meta, album_extra, comment_total, hot_comment_total):
    sql = """
            INSERT INTO album(AlbID, AlbName, ProID, ProName, School, Language, TimePub, Company, SalNum, PerPrice, Intro, SelCom, AllCom) \
            VALUES ({0}, "{1}", {2},"{3}","{4}","{5}","{6}","{7}",{8},{9},"{10}",{11},{12} )"""\
                .format(album_id, album_meta['name'], album_meta['singerid'], album_meta['singername'],\
                        album_meta['genre'], album_meta['lan'], album_meta['aDate'], album_meta['company'],\
                        album_extra['soldcount'], int(album_extra['price'])/100, album_extra['desc'], comment_total, hot_comment_total)

    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

# 插入song表
def insert_song(album_meta):
    song_list = album_meta['list']
    for song in song_list:
        if "interval" in song:
            seconds = song['interval']
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            duration = "{0}:{1}:{2}".format(h,m,s)
        song_comment_info = getCommentInfo('song', song['songmid'], song['songid'], 0, "")
        if 'comment' in song_comment_info:
            comment_total = song_comment_info['comment']['commenttotal']
        if 'hot_comment' in song_comment_info:
            hot_comment_total = song_comment_info['hot_comment']['commenttotal']
        sql = """
                INSERT INTO song(SongID, AlbID, SongName, SongDur, SSelCom, SAllCom) \
                VALUES ({0}, {1}, "{2}","{3}",{4},{5})"""\
                    .format(song['songid'], song['albumid'], song['songname'],\
                            duration, hot_comment_total, comment_total)
        print(sql)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()

# 插入comment表
def insert_comment(album_mid, album_id, comment_total):
    pagenums = comment_total//25
    lasthotcommentid = ""
    for i in range(pagenums+1):
        album_comment_info = getCommentInfo('album', album_mid, album_id, i, lasthotcommentid)
        comments = album_comment_info['comment']['commentlist']
        if not comments or len(comments) <= 0:
            break
        print("insert to comment table, pagenum:{}".format(i))
        lasthotcommentid = comments[-1]["commentid"]
        for comment in comments:
            if "middlecommentcontent" in comment and comment['middlecommentcontent'] and len(comment['middlecommentcontent']) > 0:
                content = comment['middlecommentcontent'][0]['subcommentcontent']
            elif "rootcommentcontent" in comment:
                content = comment["rootcommentcontent"]
            sql = """
                    INSERT INTO comment(ComID, AlbID, FanID, ComCont, Label, Time, Likes) \
                    VALUES ("{0}", {1}, "{2}","{3}","{4}",FROM_UNIXTIME({5}),{6} )"""\
                        .format(comment['commentid'], album_id, comment['uin'], content,\
                                comment['is_hot_cmt'], comment['time'], comment['praisenum'])
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()

# 插入fans表
def insert_fans(album_mid, album_id, actid):
    begin = 0
    end = 24
    album_rank_info = getAlbumRank(album_mid, actid, begin, end)
    while album_rank_info and album_rank_info['uin_rank_peract_288'] and album_rank_info['uin_rank_peract_288_day']:
        for rank_info in album_rank_info['uin_rank_peract_288']:
            sql = """
                    INSERT INTO fans(FanID, AlbID, `Rank`, Label, FanName, ContriValue) \
                    VALUES ("{0}", {1}, {2},{3},"{4}",{5})"""\
                        .format(rank_info['uUin'], album_id, rank_info['iRank'], 1,\
                                rank_info['strNick'], rank_info['iScore'])
            print(sql)
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()
        for rank_info in album_rank_info['uin_rank_peract_288_day']:
            sql = """
                    INSERT INTO fans(FanID, AlbID, `Rank`, Label, FanName, ContriValue) \
                    VALUES ("{0}", {1}, {2},{3},"{4}",{5})"""\
                        .format(rank_info['uUin'], album_id, rank_info['iRank'], 2,\
                                rank_info['strNick'], rank_info['iScore'])
            print(sql)
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()
        if len(album_rank_info['uin_rank_peract_288']) < 25 and len(album_rank_info['uin_rank_peract_288_day']) < 25:
            break
        begin += 25
        end += 25
        album_rank_info = getAlbumRank(album_mid, actid, begin, end)


if __name__ == "__main__":
    # 从控制台输入album_url
    album_url = input("album_url:")
    album_mid = album_url.lstrip('https://y.qq.com/n/yqq/album/').rstrip('.html')
    #album_mid = "001T7G8z0o9FlF"  # album的url后缀
    if album_mid == "":
        print("illegal album_url, please check!")
        raise RuntimeError('illegal url')
    cursor = db.cursor()
    album_meta = getAlbumInfo(album_mid)
    if 'id' in album_meta:
        album_id = album_meta['id']
        album_extra = getAlbumExtra(album_mid, album_id)
        album_acturl = getActURL(album_mid, album_id)
        actid = album_acturl['actid']
        album_comment_info = getCommentInfo('album', album_mid, album_id, 0, "")
        if 'comment' in album_comment_info:
            comment_total = album_comment_info['comment']['commenttotal']
        if 'hot_comment' in album_comment_info:
            hot_comment_total = album_comment_info['hot_comment']['commenttotal']
    #-------------------------------------------#
    # start album table
    print("--start inserting album table--")
    insert_album(album_meta, album_extra, comment_total, hot_comment_total)
    print("--finsh inserting album table--")
    #-------------------------------------------#
    # start fans table
    print("--start inserting fans table--")
    insert_fans(album_mid, album_id, actid)
    print("--finish inserting fans table--")
    #-------------------------------------------#
    # start song table
    print("--start inserting song table--")
    insert_song(album_meta)
    print("--finish inserting song table--")
    #-------------------------------------------#
    # start comment table
    print("--start inserting comment table--")
    insert_comment(album_mid, album_id, comment_total)
    print("--finish inserting comment table--")
    #-------------------------------------------#
    db.close()
