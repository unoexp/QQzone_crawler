import os
import re
from urllib import parse
import requests

headers = {'host': 'h5.qzone.qq.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'zh,zh-CN;q=0.8,en-US;q=0.5,en;q=0.3',
           'Accept-Encoding': 'gzip, deflate, br',
           'Cookie': '',
           'connection': 'keep-alive'}
hea = {'host': 'user.qzone.qq.com',
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Language': 'zh,zh-CN;q=0.8,en-US;q=0.5,en;q=0.3',
       'Accept-Encoding': 'gzip, deflate, br',
       'Cookie': '',
       'connection': 'keep-alive'}


def get_cookie():
    with open('cookie_file') as f:
        cookie = f.read()
    try:
        d = eval(cookie)
        cookie = ''
        for x in d:
            cookie += x + '=' + d[x] + '; '
    except:
        cookie = cookie.replace('\n', '')
    return cookie


def calc_cookie():
    global cookie
    global g_tk
    cookie = get_cookie()
    g_tk = get_g_tk()
    headers['Cookie'] = cookie
    hea['Cookie'] = cookie


def bkn(p_skey):
    # 计算bkn
    h = 5381
    for s in p_skey:
        h += (h << 5) + ord(s)
    return h & 2147483647


def get_g_tk():
    with open('cookie_file') as f:
        tex = f.read()
    if 'p_skey=' in tex:
        pskey_start = cookie.find('p_skey=')
        pskey_end = cookie.find(';', pskey_start)
        p_skey = cookie[pskey_start + 7: pskey_end]
        return bkn(p_skey)
    elif 'p_skey' in tex:
        try:
            tex = eval(tex)
        except:
            exit('cookie文件格式有误')
        return bkn(tex['p_skey'])
    else:
        exit('请检查cookie文件是否正确')


def get_qzonetoken(qqnum):
    index_url = "https://user.qzone.qq.com/%s" % qqnum
    res = requests.get(index_url, headers=hea)
    src = res.text
    search_res = re.search(r'g_qzonetoken.*"(.*)";}', src, re.S)
    return search_res.group(1) if search_res else ''


def parse_moods_url(qqnum):
    params = {"cgi_host": "http://taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6",
              "code_version": 1,
              "format": "jsonp",
              "g_tk": g_tk,
              "hostUin": qqnum,
              "inCharset": "utf-8",
              "need_private_comment": 1,
              "notice": 0,
              "num": 20,
              "outCharset": "utf-8",
              "sort": 0,
              "uin": qqnum}
    host = "https://h5.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?"

    url = host + parse.urlencode(params)
    return url


def parse_friends_url():
    cookie = headers['Cookie']
    qq_start = cookie.find('uin=o')
    qq_end = cookie.find(';', qq_start)
    qq_num = cookie[qq_start + 5: qq_end]
    if qq_num[0] == 0:
        qq_num = qq_num[1:]
    # 先获取qzonetoken
    qzonetoken = get_qzonetoken(qq_num)
    params = {"uin": qq_num,
              "fupdate": 1,
              "action": 1,
              "g_tk": g_tk,
              "qzonetoken": qzonetoken}

    host = "https://h5.qzone.qq.com/proxy/domain/base.qzone.qq.com/cgi-bin/right/get_entryuinlist.cgi?"
    url = host + parse.urlencode(params)
    return url


def parse_visitor(qq):
    cookie = headers['Cookie']
    qq_start = cookie.find('uin=o')
    qq_end = cookie.find(';', qq_start)
    qqnumber = cookie[qq_start + 5: qq_end]
    if qqnumber[0] == 0:
        qqnumber = qqnumber[1:]
    # 先获取qzonetoken
    qzonetoken = get_qzonetoken(qqnumber)
    params = {"uin": qq,
              'mask': 2,
              "g_tk": g_tk,
              'page': 1,
              "fupdate": 1,

              "qzonetoken": qzonetoken}

    host = "https://h5.qzone.qq.com/proxy/domain/g.qzone.qq.com/cgi-bin/friendshow/cgi_get_visitor_simple?"
    url = host + parse.urlencode(params)
    print(url)
    return url


def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


def ptqrToken(qrsig):
    # 计算ptqrtoken
    n, i, e = len(qrsig), 0, 0

    while n > i:
        e += (e << 5) + ord(qrsig[i])
        i += 1

    return 2147483647 & e
