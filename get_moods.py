#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
把包含动态的文件下载下来
"""


import requests
import os
import sys
import time
import util
import datetime

class Get_moods(object):
    '''Get moods file with cookie'''

    def __init__(self,qqi):
        self.session = requests.Session()
        self.headers = util.headers
        self.g_tk = util.g_tk
        self.qq=qqi
        self.timen=str(datetime.datetime.now())[:10]
    def single(self):
        qqnumber=self.qq
        referer = 'http://user.qzone.qq.com/' + qqnumber
        self.headers['Referer'] = referer
        util.check_path('s/'+self.timen+'/'+qqnumber+'/')
        url_base = util.parse_moods_url(qqnumber)
        pos = 0
        key = True
        
        while key:
            print("\t正在获取 第:\t%d" % ((pos+20)//20)+'页')
            url = url_base + "&pos=%d" % pos
            res = self.session.get(url, headers = self.headers)
            con = res.text
            with open('s/'+self.timen+'/'+ qqnumber + '/' + str(pos), 'w', encoding="utf-8") as f:
                
                f.write(con)
                if os.path.getsize('s/'+self.timen+'/'+ qqnumber + '/' + str(pos))/1024<2:
                    
                    break
                
            if '''"msglist":null''' in con:
                key = False
            
            pos += 20
            time.sleep(1)
    def compare(self):
        qqnumber=self.qq
        referer = 'http://user.qzone.qq.com/' + qqnumber
        self.headers['Referer'] = referer
        util.check_path('s/'+self.timen+'/'+qqnumber+'/')
        url_base = util.parse_moods_url(qqnumber)
        pos = 0
        key = True
        url = url_base + "&pos=%d" % pos
        res = self.session.get(url, headers = self.headers)
        con = res.text
        qaq=0
        tm=0
        while True:
            
            with open('s/'+self.timen+'/'+ qqnumber + '/' + str(pos), 'r', encoding="utf-8") as f:
                co=f.read()
                if not con==co:
                    util.check_path('s/'+self.timen+'/'+ qqnumber + '/10/')
                    with open('s/'+self.timen+'/'+ qqnumber + '/10/' + str(qaq), 'w', encoding="utf-8") as f:    
                        f.write(con)
                        qaq+=1
                        with open('s/'+self.timen+'/'+ qqnumber + '/' + str(pos), 'w', encoding="utf-8") as f:
                            f.write(con)
                        print('替换一次!!!!!!!')
                        pygame.mixer.init()
                        
                        track = pygame.mixer.music.load("dontmove/bing.mp3")
                        pygame.mixer.music.play() 

            tm+=1
            print('已检查'+str(tm)+'次')
            time.sleep(60) #检查周期
            
            
    def get_moods(self,qqnumber):
        '''Use cookie and header to get moods file and save it to result folder with QQnumber name'''
        
        referer = 'http://user.qzone.qq.com/' + qqnumber
        self.headers['Referer'] = referer

        # Create a folder with qq number to save it's result file
        util.check_path('al/'+self.timen+'/' +qqnumber)

        # Get the goal url, except the position argument.
        url_base = util.parse_moods_url(qqnumber)

        pos = 0
        key = True

        while key:
            print("\t正在获取 第:\t%d" % ((pos+20)//20)+'页')
            url = url_base + "&pos=%d" % pos
            # print(url)   # for debug use
            res = self.session.get(url, headers = self.headers)
            con = res.text
            with open('al/'+self.timen+'/'+ qqnumber + '/' + str(pos), 'w', encoding="utf-8") as f:
                f.write(con)

            if '''"msglist":null''' in con:
                key = False

            # Cannot access...
            if '''"msgnum":0''' in con:
                with open('crawler_log.log', 'a', encoding="utf-8") as log_file:
                    log_file.write("%s Cannot access..\n" % qqnumber)
                key = False

            # Cookie expried
            if '''"subcode":-4001''' in con:
                with open('crawler_log.log', 'a', encoding="utf-8") as log_file:
                    log_file.write('Cookie Expried! Time is %s\n' % time.ctime())
                sys.exit()

            pos += 20
            time.sleep(1)

    #below method only make for me to get the friend's mood
    #which havn't download yet.
    #
    #def get_rest_number(self):

    #    exists_number = os.listdir('mood_result')
    #    with open('qqnumber_backup.inc') as f:
    #        con = f.read()
    #    con = eval(con)
    #    for item in con:
    #        qq = item['data']
    #        if qq not in exists_number:
    #            print("Dealing with:\t%s" % qq)
    #            self.get_moods(qq)
    #    else:
    #        print('Finish!')


class Get_moods_start(object):

    def __init__(self,qqi):
        print('开始获取id')
        self.qq=qqi
        self.timen=str(datetime.datetime.now())[:10]
    def get_moods_start(self,a):
        app = Get_moods(self.qq)
        #app.get_rest_number()

        with open('qqnumber.inc', encoding="utf-8") as qnumber_file:
            qnumber_string = qnumber_file.read()
        qnumber_list = eval(qnumber_string)

        # check if there is a mood_result folder to save the result file
        # if not create it
        util.check_path('s/'+self.timen+'/'+self.qq+'/' if a==1 else 'al/'+self.timen+'/')
        if a==1 :
            app.single()
            print('完成')
        else:
            
            while qnumber_list != []:
                save_back_qnumber = qnumber_list[:]
                item = qnumber_list.pop()
                qq = item['data']
                print("正在处理:\t%s" % qq)
    
                start_time = time.ctime()
                with open('crawler_log.log', 'a', encoding="utf-8") as log_file:
                    log_file.write("Program run at: %s\tGetting %s data...\n" % (start_time, qq))
    
                try:
                    app.get_moods(qq)
                except KeyboardInterrupt:
                    print('User Interrupt, program will exit')
                    sys.exit()
                except Exception as e:
                    # Write the rest item back to qqnumber.inc
                    with open('qqnumber.inc', 'w', encoding="utf-8") as qnumber_file:
                        qnumber_file.write(str(save_back_qnumber))
    
                    # Write the log
                    with open('crawler_log.log', 'a', encoding="utf-8") as log_file:
                        exception_time = time.ctime()
                        log_file.write("Exception occured: %s\n%s\n" % (exception_time, e))
                else:
                    print("%s 已完成" % qq)
            else:
                print("全部完成")
