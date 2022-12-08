import datetime
import json
import os
import shutil
import time

import util

date_today = str(datetime.datetime.now())[:10]


# emoji

def emoji2pic(a):
    if '[em]' in a:
        while '[em]' in a:
            try:
                l = a.index('[em]')
                r = a.index('[/em]')
                em = a[l + 4:r]
                a = a[:l] + '<img class="emojy" src="http://qzonestyle.gtimg.cn/qzone/em/' + em + '.gif">' + a[r + 5:]
            except:
                break
    return a


class Get_detail(object):

    def __init__(self, inp, ti):
        self.pos_count = 0
        self.countt = 0
        self.inp = inp
        self.timen = ti
        self.year = []
        self.count = []
        self.tyear = []
        self.t = []
        self.list_count = 0

    def make_dict(self, a, qq_num, date_):
        mood_dict = dict()
        if a == 1:
            dir_path = os.path.join('content', 'single', date_)
        elif qq_num is None:
            dir_path = os.path.join('content', 'all', date_)
        else:
            dir_path = os.path.join('content', 'all', date_, qq_num)
        dir_list = os.listdir(dir_path)
        for d in dir_list:
            if a == 1 or qq_num is None:
                file_list = os.path.join(dir_path, d)
            else:
                file_list = os.path.join(dir_path, qq_num)
            if len(file_list) != 1:
                mood_dict[d] = file_list
        return mood_dict

    def exact_mood_data(self, qq_num, file_name):
        self.pos_count = 0
        with open(file_name, encoding="utf-8") as f:
            content = f.read()
        try:
            con_dict = json.loads(content[10:-2])
            moods = con_dict['msglist']
        except:
            return

        if moods is None:
            return
        mood_item = dict()
        mood_item['belong'] = qq_num

        # 单条说说
        for mood in moods:
            if 'rt_source' in mood:
                mood_item['content'] = '转发&nbsp&nbsp&nbsp&nbsp' + mood['content'] + '<br>原文内容↓<br>' + '[' + str(
                    mood['rt_uin']) + ']:' + mood['rt_con']['content']  # 转发为真
            else:
                mood_item['content'] = mood['content']  # 内容
            mood_item['createTime'] = mood['createTime']  # 创建时间
            time_st = stime(mood['created_time'])
            mood_item['created_time'] = str(time_st[0])  # 精确时间

            if not time_st[1] in self.tyear:
                self.tyear.append(time_st[1])
                emptylist = []
                self.t.append(emptylist)
                temp_list = [time_st[2], 1]
                self.t[self.list_count].append(temp_list)
                self.list_count += 1
            else:
                for i in range(0, len(self.t[self.list_count - 1])):
                    if not time_st[2] == self.t[self.list_count - 1][i][0]:
                        if i == len(self.t[self.list_count - 1]) - 1:
                            temp_list = [time_st[2], 1]
                            self.t[self.list_count - 1].append(temp_list)
                    else:
                        self.t[self.list_count - 1][i][1] += 1
                        break
            if not mood_item['created_time'][:5] in self.year:
                self.year.append(mood_item['created_time'][:5])
                self.count.append(0)
                self.count[self.year.index(mood_item['created_time'][:5])] += 1
            else:
                self.count[self.year.index(mood_item['created_time'][:5])] += 1

            mood_item['com_num'] = mood['cmtnum']  # 评论数
            mood_item['phone'] = mood['source_name']  # 设备名
            mood_item['rt'] = mood['rt_sum']  # 累计转发
            # video
            video = False
            if 'video' in mood:
                video = True
                try:
                    mood_item['video'] = mood['video'][0]['url3']
                    print(mood_item['video'])
                except:
                    pass

            # pic
            pic = 0
            pic_total = 0
            try:
                pic_total = mood['pictotal']
                for pic in range(0, pic_total):
                    mood_item['pic' + str(pic)] = mood['pic'][pic]['url2']
            except:
                pass
            # pic end
            mood_item['locate'] = mood['story_info']['lbs']['name'] if 'story_info' in mood else ''  # 位置名称
            mood_item['loc_pos_x'] = mood['story_info']['lbs']['pos_x'] if 'story_info' in mood else ''  # pos_x
            mood_item['loc_pos_y'] = mood['story_info']['lbs']['pos_y'] if 'story_info' in mood else ''  # pos_y
            # 评论
            templ = 0

            for tempc in range(0, mood['cmtnum']):  # 评论循环
                if mood['commentlist'] == 'null':  # 没有评论
                    mood_item['commuin' + str(tempc)] = None  # 评论uin
                    mood_item['comm' + str(tempc)] = None  # 评论内容
                    mood_item['commt' + str(tempc)] = None  # 评论时间
                else:
                    try:
                        lenlis = len(mood['commentlist'][tempc]['list_3'])
                    except:
                        lenlis = None
                    try:
                        mood_item['commuin' + str(tempc)] = mood['commentlist'][tempc]['uin']  # 评论tempc的uin
                        mood_item['repic'] = None
                        if 'pic' in mood['commentlist'][tempc]:
                            mood_item['repic'] = mood['commentlist'][tempc]['pic'][0]['b_url']
                        mood_item['comm' + str(tempc)] = mood['commentlist'][tempc]['content']  # 评论内容
                        mood_item['commt' + str(tempc)] = mood['commentlist'][tempc]['createTime2']  # 评论时间
                    except:
                        break
                    if lenlis == None:  # 是否有回复评论
                        # print(lenlis)
                        mood_item['commre' + str(templ)] = None
                        mood_item['commrename' + str(templ)] = None
                    else:
                        for templ in range(0, lenlis):  # 回复循环
                            mood_item['rerepic'] = None
                            if 'pic' in mood['commentlist'][tempc]['list_3'][templ]:
                                mood_item['rerepic'] = mood['commentlist'][tempc]['list_3'][templ][0]['pic']['b_url']
                            mood_item['commre' + str(tempc) + str(templ)] = mood['commentlist'][tempc]['list_3'][templ][
                                'content']  # 楼中楼内容try:
                            mood_item['commrename' + str(tempc) + str(templ)] = \
                                mood['commentlist'][tempc]['list_3'][templ]['uin']  # 楼中楼人
                            mood_item['commtime' + str(tempc) + str(templ)] = \
                                mood['commentlist'][tempc]['list_3'][templ]['createTime2']  # time

            if self.inp == '1':
                f = open(os.path.join('result', 'single_html', qq_num, self.timen + '.html'), 'a', encoding='utf-8')
            else:
                f = open(os.path.join('result', 'all_html', self.timen, qq_num + '.html'), 'a', encoding='utf-8')

            f.write('<div class="item"><div class="text">' + emoji2pic(mood_item['content']) + '</div>')

            for pic in range(0, pic_total):
                try:
                    f.write('<br>' + '&nbsp&nbsp<img class="pic" src="' + str(
                        mood_item['pic' + str(pic)]) + '"' +  '>')
                except:
                    break
            if video:
                try:
                    f.write("<br><video src=\"" + mood_item['video'] + "\" controls=\"controls\"></video>")
                except:
                    pass
            f.write('<br>精确时间&nbsp&nbsp ' + str(mood_item['created_time']) + '<br>相对时间&nbsp&nbsp' + str(
                mood_item['createTime']) + '<br>评论数     ' + str(mood_item['com_num']))
            f.write('<br>设备名&nbsp&nbsp' + str(mood_item['phone']) + '<br>累计转发&nbsp' + str(mood_item['rt']))
            if mood_item['locate'] != '':
                f.write('<br>位置名称&nbsp' + str(mood_item['locate']))
            if mood_item['loc_pos_x'] != '' or mood_item['loc_pos_y'] != '':
                f.write('<br>维度' + str(mood_item['loc_pos_x']) + '<br>经度' + str(mood_item['loc_pos_y']))

            for tempc in range(0, min(10,mood['cmtnum'])):
                try:
                    lenlis = len(mood['commentlist'][tempc]['list_3'])  # 楼中楼num
                except:
                    lenlis = None
                try:
                    f.write('<br><br>')
                    # head pic
                    f.write('<img class="qlogo" src=http://qlogo1.store.qq.com/qzone/' + str(
                        mood_item['commuin' + str(tempc)]) + '/' + str(
                        mood_item['commuin' + str(tempc)]) + '/30>' + str(mood_item['commuin' + str(tempc)]))

                    f.write('<div class="text"><br>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' + str(
                        emoji2pic(mood_item['comm' + str(tempc)])) + '</div>')
                    if 'pic' in mood['commentlist'][tempc]:
                        f.write('<br><img class="pic" src=' + mood['commentlist'][tempc]['pic'][0][
                            'hd_url'] + '>')
                    f.write('<br>&nbsp&nbsp时间' + str(mood_item['commt' + str(tempc)]))
                except:
                    pass
                try:
                    for templ in range(0, lenlis):
                        f.write(
                            '<br>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<img class="qlogo" src=http://qlogo1.store.qq.com/qzone/' + str(
                                mood_item['commrename' + str(tempc) + str(templ)]) + '/' + str(
                                mood_item['commrename' + str(tempc) + str(templ)]) + '/30>')
                        f.write('&nbsp&nbsp' + str(mood_item['commrename' + str(tempc) + str(templ)]))  # 楼中楼人

                        f.write('<div class="text"><br>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' + str(
                            emoji2pic(mood_item['commre' + str(tempc) + str(templ)])) + '</div>') # 楼中楼内容
                        if not mood_item['rerepic'] == None:
                            f.write('<img class="pic" src=' + mood_item[
                                'rerepic'] + '>')
                        f.write('<br>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp评论时间' + str(
                            mood_item['commtime' + str(tempc) + str(templ)]))
                except:
                    pass
            f.write('</div>')
            f.close()
            self.pos_count += 1
            self.countt += 1
            print('正在处理，计数为： ' + str(self.countt))


def time1(qq_num, year, count):
    util.check_path(os.path.join('report', qq_num))
    f = open(os.path.join('report', qq_num, 'time1.html'), 'w', encoding='utf-8')

    shutil.copyfileobj(open(os.path.join('resources', 'time1.part1'), 'r'), f)
    f.write(str(year))
    shutil.copyfileobj(open(os.path.join('resources', 'time1.part2'), 'r'), f)
    f.write(str(count))
    shutil.copyfileobj(open(os.path.join('resources', 'time1.part3'), 'r'), f)
    for i in range(0, len(year)):
        f.write("{name:'" + str(year[i]) + "',value:" + str(count[i]) + '}')
        if i != len(year) - 1:
            f.write(',')
    shutil.copyfileobj(open(os.path.join('resources', 'time1.part4'), 'r'), f)
    f.close()


def time2(qq_num, y, t):
    util.check_path('report/' + str(qq_num) + '/')
    f = open(os.path.join('report', qq_num, 'time2.html'), 'w', encoding='utf-8')

    shutil.copyfileobj(open(os.path.join('resources', 'time2.part1'), 'r'), f)
    f.write(str(y))
    shutil.copyfileobj(open(os.path.join('resources', 'time2.part2'), 'r'), f)
    for i in range(0, len(y)):
        shutil.copyfileobj(open(os.path.join('resources', 'time2.part3'), 'r'), f)
        f.write("'" + str(y[i]) + "',")
        shutil.copyfileobj(open(os.path.join('resources', 'time2.part4'), 'r'), f)
        f.write(str(t[i]))
        shutil.copyfileobj(open(os.path.join('resources', 'time2.part5'), 'r'), f)
    shutil.copyfileobj(open(os.path.join('resources', 'time2.part6'), 'r'), f)
    f.close()


def stime(a):
    b = str(time.ctime(a))
    re = b[-4:] + '年'
    te = b[4:]
    e = te[:3]
    d = {
        'Jan': '1月',
        'Feb': '2月',
        'Mar': '3月',
        'Apr': '4月',
        'May': '5月',
        'Jun': '6月',
        'Jul': '7月',
        'Aug': '8月',
        'Sep': '9月',
        'Oct': '10月',
        'Nov': '11月',
        'Dec': '12月'
    }
    re = re + d[e]
    te = te[:-5]
    re = re + str(te[4:-9]) + '日'
    te = te[-8:]

    res = [re + ' ' + te]
    re = re.replace('年', '/')
    re = re.replace('月', '/')
    re = re.replace('日', '')
    res.append(re[:4])
    re = re[5:]
    res.append(re)
    res.append(te[:-3])
    return res


# def auto_collect(qq_num):
#     date_ = date_today
#     pos = 0
#     app = Get_detail('1', date_)
#     mood_dict = app.make_dict(1, qq_num, date_)
#     util.check_path(os.path.join('result', 'single_html', qq_num))
#     raw_path = os.path.join('content', 'single', date_, qq_num)
#     res_path = os.path.join('result', 'single_html', qq_num, date_ + '.html')
#     with open(res_path, 'w', encoding='utf-8') as f:
#         f.write('<body>')
#     for dirName, fileName in mood_dict.items():
#         for each_file in fileName:
#             filename = os.path.join(raw_path, str(pos))
#             # 所有文件已经读取完毕
#             if not os.path.exists(filename):
#                 break
#             app.exact_mood_data(qq_num, filename)
#             year = app.year
#             count = app.count
#             pos += 20
#     print('正在处理数据...')
#     for s in range(0, len(app.t)):
#         for m in range(0, len(app.t[s])):
#             app.t[s][m][0] = app.tyear[s] + '/' + app.t[s][m][0]
#     time1(qq_num, year, count)
#     time2(qq_num, app.tyear, app.t)


# -----------------------------------main------------------------------------

def main(auto=0, qq_num=0):
    if auto == 1:
        inp = '1'
        date_ = date_today
    elif auto == 2:
        inp = '2'
        date_ = date_today
    else:
        inp = input('\n......\n1：整理单人\n2：整理所有人\n')
        if inp == '1':
            qq_num = input('\n输入...id\n')
            qq_num = str(qq_num)  # tim UIN
        date_ = input('\n......\n1：整理今天的\n2：整理以前的【输入文件夹名】\n')
        while len(date_) != 10 and date_ != '1':
            date_ = input('\n输入日期有错误, 请复制文件夹名, 例如2022-02-02\n')
        if date_ == '1':
            date_ = date_today

    if inp == '1':
        # s文件夹里没有, 去al文件夹里找找
        raw_path = os.path.join('content', 'single', date_, qq_num)
        if not os.path.exists(raw_path):
            raw_path = os.path.join('content', 'all', date_, qq_num)
            if not os.path.exists(raw_path):
                print('未找到文件夹 请先获取')
                exit(0)

        pos = 0
        app = Get_detail(inp, date_)
        mood_dict = app.make_dict(1, qq_num, date_)
        util.check_path(os.path.join('result', 'single_html', qq_num))

        res_path = os.path.join('result', 'single_html', qq_num, date_ + '.html')
        with open(res_path, 'w', encoding='utf-8') as f:
            f.write('<!doctype html><head><meta charset = "UTF-8">')
            f.write('<title>' + qq_num + '</title>')
            f.write('<link rel="stylesheet" href="../../../resources/css.css">')
            f.write('</head>')
            f.write('<body>')

        for dirName, fileName in mood_dict.items():
            for each_file in fileName:
                filename = os.path.join(raw_path, str(pos))
                # 所有文件已经读取完毕
                if not os.path.exists(filename):
                    break
                app.exact_mood_data(qq_num, filename)
                pos += 20  # 2018.10.3更新 说说将按时间顺序排布
        with open(res_path, 'a', encoding='utf-8') as f:
            f.write('</body>')
        print('正在处理数据...')
        for s in range(0, len(app.t)):
            for m in range(0, len(app.t[s])):
                app.t[s][m][0] = app.tyear[s] + '/' + app.t[s][m][0]
        time1(qq_num, app.year, app.count)
        time2(qq_num, app.tyear, app.t)
    else:
        util.check_path(os.path.join('result', 'all_html', date_))
        pos = 0
        app = Get_detail(None, date_)
        mood_dict = app.make_dict(0, None, date_)
        for dirName, fileName in mood_dict.items():
            res_path = os.path.join('result', 'all_html', date_, dirName + '.html')
            with open(res_path, 'w', encoding='utf-8') as f:
                f.write('<!doctype html><head><meta charset = "UTF-8">')
                f.write('<title>' + dirName + '</title>')
                f.write('<link rel="stylesheet" href="../../../resources/css.css">')
                f.write('</head>')
                f.write('<body>')

            for each_file in fileName:
                filename = os.path.join('content', 'all', date_, dirName, str(pos))
                # 所有文件已经读取完毕
                if not os.path.exists(filename):
                    break
                app.exact_mood_data(dirName, filename)
                pos += 20
            with open(res_path, 'a', encoding='utf-8') as f:
                f.write('</body>')
            for s in range(0, len(app.t)):
                for m in range(0, len(app.t[s])):
                    app.t[s][m][0] = app.tyear[s] + '/' + app.t[s][m][0]
            time1(str(dirName), app.year, app.count)
            time2(str(dirName), app.tyear, app.t)
            print(dirName + ' 已完成')
            pos = 0
            app = Get_detail(inp, date_)
    print('整理完成!')


# -----------------------------------/main------------------------------------


if __name__ == '__main__':
    main()
