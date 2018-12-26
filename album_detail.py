#-*- coding:utf-8 -*-
import requests
import json

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
def getCommentInfo(album_mid, top_id):
    url = 'https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg'
    header = {
        'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'referer':'https://y.qq.com/n/yqq/album/{}.html'.format(album_mid)
    }
    paramters = {
        'g_tk':'5381',
        'topid':'{}'.format(top_id), #传入top_id
        'cmd':'8',
        'cid':'205360772',
        'reqtype':'2',
        'jsonpCallback':'jsonp1',
        'biztype':'2',
        'domain':'qq.com',
        'ct':'24',
        'cv':'101010',
        'loginUin':'0',
        'hostUin':'0',
        'format':'json',
        'inCharset':'utf8',
        'outCharset':'GB2312',
        'needmusiccrit':'0',
        'pagenum':'0',
        'pagesize':'25',
        'notice':'0',
        'platform':'yqq.json',
        'lasthotcommentid':'',
        'needNewCode':'0'
    }
    html = requests.get(url=url,params=paramters,headers=header)
    res = json.loads(html.text.strip())
    return res

if __name__ == "__main__":
    # 从控制台输入album_url
    album_url = input("album_url:")
    album_mid = album_url.lstrip('https://y.qq.com/n/yqq/album/').rstrip('.html')
    #album_mid = "004KHjpn0p4Az7"  # album的url后缀
    album_meta = getAlbumInfo(album_mid)
    if 'id' in album_meta:
        album_id = album_meta['id']
        album_info = getAlbumExtra(album_mid, album_id)
        album_acturl = getActURL(album_mid, album_id)
        actid = album_acturl['actid']
        album_rank = getAlbumRank(album_mid,actid, 0,24)
        album_comment_info = getCommentInfo(album_mid, album_id)
        if 'comment' in album_comment_info:
            comment_total = album_comment_info['comment']['commenttotal']
        if 'hot_comment' in album_comment_info:
            hot_comment_total = album_comment_info['hot_comment']['commenttotal']
        print(comment_total)
        print(hot_comment_total)
