#-*- coding:utf-8 -*-
import requests
import json

#获取专辑id
def getAlbumID(album_mid):
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
        'format':'jsonp',
        'inCharset':'utf8',
        'outCharset':'utf-8',
        'notice':'0',
        'platform':'yqq.json',
        'needNewCode':'0'
    }

    html = requests.get(url=url,params=paramters,headers=header)
    res = json.loads(html.text.strip().lstrip('jsonp1(').rstrip(')'))['data']
    if 'id' in res:
        album_id = res['id']
        album_info = getAlbumInfo(album_mid, album_id)
        album_acturl = getActURL(album_mid, album_id)
        actid = album_acturl['actid']
        album_rank = getAlbumRank(album_mid,actid, 0,24)
        print(album_rank)
    else:
        return

#获取专辑信息
def getAlbumInfo(album_mid, album_id):
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
        'format':'jsonp',
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


def getAlbumRank(album_mid, actid, begin, end):
    url = 'https://c.y.qq.com/shop/fcgi-bin/fcg_album_rank'
    header = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'referer':'https://y.qq.com/n/yqq/album/{}.html'.format(album_mid)
    }
    rankname = "uin_rank_peract_{0}|uin_rank_peract_{0}_day".format(actid)
    print(rankname)
    paramters = {
        'begin':'{}'.format(begin),
        'end':'{}'.format(end),
        'rankname':rankname,
        'g_tk':'5381',
        'p':'0.8575604667634174',
        'jsonpCallback':'jsonp1',
        'loginUin':'0',
        'hostUin':'0',
        'format':'jsonp',
        'inCharset':'utf8',
        'outCharset':'utf-8',
        'notice':'0',
        'platform':'yqq.json',
        'needNewCode':'0'
    }
    print(paramters)

    html = requests.get(url=url,params=paramters,headers=header)
    res = json.loads(html.text.strip().lstrip('jsonp1(').rstrip(')'))
    if 'data' in res:
        return res['data']
    else:
        return {}

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
        'format':'jsonp',
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


if __name__ == "__main__":
    getAlbumID("001T7G8z0o9FlF")
