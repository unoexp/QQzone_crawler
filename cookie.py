from PIL import Image
import re
import requests
import threading
import time
import util

get_img_url = 'https://ssl.ptlogin2.qq.com/ptqrshow'
check_img_url = 'https://xui.ptlogin2.qq.com/ssl/ptqrlogin'
qrsig = ''


class get_QR(threading.Thread):
    def run(self):
        param = {
            'appid': '549000912',
            'e': '2',
            'I': 'M',
            's': '3',
            'd': '72',
            'v': '4',
            't': '0.35588189253347835',
            'daid': '5',
            'pt_3rd_aid': '0'
        }
        QR = requests.get(get_img_url, params=param)
        global qrsig
        qrsig = requests.utils.dict_from_cookiejar(QR.cookies).get('qrsig')
        f = open('QR.png', 'wb+')
        f.write(QR.content)
        im = Image.open(f)
        print('已展示二维码')
        im.show()


def get_cookie():
    t = get_QR()
    t.start()
    while qrsig == '':
        time.sleep(1)
    cookies = {
        'qrsig': qrsig
    }
    param = {
        'u1': 'https://qzs.qzone.qq.com/qzone/v5/loginsucc.html?para=izone',
        'ptqrtoken': util.ptqrToken(qrsig),
        'ptredirect': '0',
        'h': '1',
        't': '1',
        'g': '1',
        'from_ui': '1',
        'ptlang': '2052',
        'action': '0-0-' + str(time.time()),
        'js_ver': '22080914',
        'js_type': '1',
        'login_sig': '',
        'pt_uistyle': '40',
        'aid': '549000912',
        'daid': '5'
    }
    while True:
        res = requests.get(check_img_url, params=param, cookies=cookies)
        if '二维码' in res.text:
            print(res.text)
        else:
            print('登录成功, 请关闭二维码')

            cookies = requests.utils.dict_from_cookiejar(res.cookies)
            uin = requests.utils.dict_from_cookiejar(res.cookies).get('uin')
            regex = re.compile(r'ptsigx=(.*?)&')
            sigx = re.findall(regex, res.text)[0]
            url = 'https://ptlogin2.qzone.qq.com/check_sig?pttype=1&uin=' + uin + \
                  '&service=ptqrlogin&nodirect=0&ptsigx=' + sigx + \
                  '&s_url=https%3A%2F%2Fqzs.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone&f_url=&ptlang=2052&ptredirect=100&aid=549000912&daid=5&j_later=0&low_login_hour=0&regmaster=0&pt_login_type=3&pt_aid=0&pt_aaid=16&pt_light=0&pt_3rd_aid=0'

            try:
                r = requests.get(url, cookies=cookies, allow_redirects=False)
                targetCookies = requests.utils.dict_from_cookiejar(r.cookies)
                pSkey = requests.utils.dict_from_cookiejar(r.cookies).get('p_skey')
            except Exception as e:
                print(e)
            finally:
                break
        time.sleep(2)
    with open('cookie_file', 'w', encoding='utf-8') as f:
        f.write(str(targetCookies))
