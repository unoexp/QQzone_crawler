import requests
from time import sleep
import util


class Get_friends_number(object):
    def __init__(self):

        self.headers = util.headers
        self.base_url = util.parse_friends_url()
        util.check_path('friends')
        print('开始获取好友列表，并把文件保存到 friends 文件夹')

    def get_friends(self):

        key = True
        position = 0
        while key:
            url = self.base_url + '&offset=' + str(position)
            referer = 'http://qzs.qq.com/qzone/v8/pages/setting/visit_v8.html'
            self.headers['Referer'] = referer

            print(f'\t正在获取好友列表\t{position}.')
            res = requests.get(url, headers=self.headers)
            html = res.text
            with open('friends/offset' + str(position) + '.json', 'w', encoding='utf-8') as f:
                f.write(html)

            if "请先登录" in html:
                print("登录失败，请检查原因")
                key = False
                break
            if '"uinlist":[]' in html:
                print("好友列表获取完毕!")
                break

            position += 50
            # 防ban
            sleep(1)
