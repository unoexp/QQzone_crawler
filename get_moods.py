import requests
import os
import sys
import time
import util
import datetime


class Get_moods(object):
    def __init__(self):
        self.session = requests.Session()
        self.headers = util.headers
        self.g_tk = util.g_tk
        self.timen = str(datetime.datetime.now())[:10]

    def get_moods(self, s, qq_num):
        referer = 'http://user.qzone.qq.com/' + qq_num
        self.headers['Referer'] = referer
        if s == 'single':
            path = os.path.join('content', 'single', self.timen, qq_num)
        elif s == 'all':
            path = os.path.join('content', 'all', self.timen, qq_num)
        else:
            return

        util.check_path(path)
        url_base = util.parse_moods_url(qq_num)
        pos = 0
        key = True

        while key:
            print(f'\t正在获取 第:\t{(pos + 20) // 20}页')
            url = url_base + "&pos=%d" % pos
            res = self.session.get(url, headers=self.headers)
            con = res.text
            with open(os.path.join(path, str(pos)), 'w', encoding="utf-8") as f:
                f.write(con)

            if '"msglist":null' in con:
                key = False

            if '"subcode":2' in con:
                if s == 'single':
                    exit('对不起,主人设置了保密,您没有权限查看')
                else:
                    print(f'无法访问{qq_num}的空间')
                key = False

            if '"subcode":-10000' in con:
                print('获取中断, 使用人数过多，请稍后再试')
                key = False

            if '"msgnum":0' in con:
                key = False

            if '"subcode":-4001' in con:
                exit(f'cookie有误{time.ctime()}\n')

            pos += 20
            # 防ban
            time.sleep(1)


class Get_moods_start(object):

    def __init__(self, qqi):
        print('开始获取id')
        self.qq = qqi
        self.timen = str(datetime.datetime.now())[:10]

    def get_moods_start(self, a):
        app = Get_moods()

        with open('qqnumber.inc', encoding="utf-8") as qnumber_file:
            qnumber_string = qnumber_file.read()
        qnumber_list = eval(qnumber_string)

        if a == 1:
            util.check_path(os.path.join('content', 'single', self.timen, self.qq))
        else:
            util.check_path(os.path.join('content', 'all', self.timen))

        if a == 1:
            app.get_moods('single', self.qq)
            print('完成')
        else:
            while qnumber_list != []:
                save_back_qnumber = qnumber_list[:]
                item = qnumber_list.pop()
                self.qq = item['data']
                print(f'正在处理:\t{self.qq}')
                try:
                    app.get_moods('all', self.qq)
                except Exception as e:
                    with open('qqnumber.inc', 'w', encoding="utf-8") as qnumber_file:
                        qnumber_file.write(str(save_back_qnumber))
                else:
                    print(f'{self.qq} 已完成')
            else:
                print("全部完成")
