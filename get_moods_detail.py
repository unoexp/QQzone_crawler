#!/usr/bin/env python -*- coding:utf-8 -*-
import time
import os
import json
import html
import datetime
import util
import shutil
import re
timen=str(datetime.datetime.now())[:10]
def em(a):
        if '[em]'in a:
            while('[em]'in a):
                try:
                        po=a.index('[em]')
                        poe=a.index('[/em]')
                        em=a[po+4:poe]
                        a=a[:po]+'<img src="http://qzonestyle.gtimg.cn/qzone/em/'+em+'.gif">'+a[poe+5:]
                except:
                        break
        return a

class Get_detail(object):

    def __init__(self,inp,ti):
        self.poscount=0
        self.countt = 0
        self.inp=inp
        self.timen=ti
        self.year=[]
        self.count=[]
        self.tyear=[]
        self.t=[]
        self.listcount=0
        
    def make_dict(self,a,qq,dat):
        
        mood_dict = dict()
        dir_list = os.listdir('s/'+dat+'/' if int(a)==1 else 'al/'+dat+'/' if qq == None else 'al/'+dat+'/'+str(qq) )
        #print(dir_list)
        for d in dir_list:

                file_list = os.listdir('s/'+dat+'/' + d if int(a)==1 else 'al/' + dat+'/'+d if qq==None else  'al/' + dat+'/'+qq+'/')
                if len(file_list) != 1:
                        mood_dict[d] = file_list
        return mood_dict
        
    def exact_mood_data(self, qq, fname):
        self.poscount=0
        qqnumber = qq
        filename = fname
        with open(filename, encoding="utf-8") as f:
            con = f.read()
        try:
                con_dict = json.loads(con[10:-2])
        except:
                return
        try:
            moods = con_dict['msglist']
        except KeyError:
            return
        if moods == None:
            return
        
        mood_item = dict()
        mood_item['belong'] = qqnumber

        for mood in moods:
            
            if 'rt_source' in mood:
               mood_item['content'] = '转发&nbsp&nbsp&nbsp&nbsp'+mood['content']+'<br>原文内容↓<br>'+'['+str(mood['rt_uin'])+']:'+mood['rt_con']['content']#转发为真
            else:
               mood_item['content'] = mood['content']#内容
            mood_item['createTime'] = mood['createTime']#创建时间
            time_st=stime(mood['created_time'])
            #print(mood['created_time'])
            mood_item['created_time']=str(time_st[0])#精确时间
            #####################################
            if not time_st[1] in self.tyear:
                    self.tyear.append(time_st[1])
                    
                    emptylist=[]
                    self.t.append(emptylist)
                    temp_list=[]
                    temp_list.append(time_st[2])
                    temp_list.append(1)
                    self.t[self.listcount].append(temp_list)
                    self.listcount+=1
                    #self.t.append(1)
            else:
                for i in range(0,len(self.t[self.listcount-1])):                         
                            if not time_st[2] == self.t[self.listcount-1][i][0]:
                                    if i==len(self.t[self.listcount-1])-1:
                                            temp_list=[]
                                            temp_list.append(time_st[2])
                                            temp_list.append(1)
                                            self.t[self.listcount-1].append(temp_list)
                            else:
                                    self.t[self.listcount-1][i][1]+=1
                                    
                                    break
            #####################################
            if not mood_item['created_time'][:5] in self.year:
                    self.year.append(mood_item['created_time'][:5])
                    self.count.append(0)
                    self.count[self.year.index(mood_item['created_time'][:5])]+=1
            else:
                    self.count[self.year.index(mood_item['created_time'][:5])]+=1
            
            mood_item['com_num'] = mood['cmtnum']#评论数
            mood_item['phone'] = mood['source_name']#设备名
            mood_item['rt']=mood['rt_sum']#累计转发
            #video
            video=False
            if 'video' in mood:
                    video=True
                    try:
                            mood_item['video'] = mood['video'][0]['url3']
                            print(mood_item['video'])
                    except:
                            pass


            
            ###
            #pic
            temp=0
            pictol=0
            try:
               pictol=mood['pictotal']
               for temp in range (0,pictol):
                  try:
                          mood_item['pic'+str(temp)] = mood['pic'][temp]['url2']
                     #if 'is_video' in mood['pic'][temp]:
                     #       mood_item['pic'+str(temp)]=mood['pic'][temp]['video_info']['url3']
                     #else:
                        
                  except :
                     break
            except:
               aaa=1
            #pic end
            mood_item['locate'] = mood['story_info']['lbs']['name'] if 'story_info' in mood else '' #位置名称
            mood_item['loc_pos_x'] = mood['story_info']['lbs']['pos_x'] if 'story_info' in mood else '' #pos_x
            mood_item['loc_pos_y'] = mood['story_info']['lbs']['pos_y'] if 'story_info' in mood else '' #pos_y
            #评论
            tempc=0
            templ=0
            
            for tempc in range(0,mood['cmtnum']):#评论循环
               if mood['commentlist']=='null':#没有评论
                   mood_item['commuin'+str(tempc)]=None#评论uin
                   mood_item['comm'+str(tempc)] = None#评论内容
                   mood_item['commt'+str(tempc)] = None#评论时间
               else:
                   try:
                       lenlis=len(mood['commentlist'][tempc]['list_3'])
                   except:
                       lenlis=None
                   try:
                       mood_item['commuin'+str(tempc)]=mood['commentlist'][tempc]['uin']#评论tempc的uin
                       mood_item['repic']=None
                       if 'pic' in mood['commentlist'][tempc]:
                               
                               mood_item['repic']=mood['commentlist'][tempc]['pic'][0]['b_url']
                               
                       mood_item['comm'+str(tempc)] = mood['commentlist'][tempc]['content']#评论内容
                       
                       mood_item['commt'+str(tempc)] = mood['commentlist'][tempc]['createTime2']#评论时间
                   except:
                       break
                   if lenlis==None:#是否有回复评论
                       #print(lenlis)
                       mood_item['commre'+str(templ)]=None
                       mood_item['commrename'+str(templ)]=None
                   else:
                        for templ in range(0,lenlis):#回复循环
                            mood_item['rerepic']=None
                            if 'pic' in mood['commentlist'][tempc]['list_3'][templ]:
                               mood_item['rerepic']=mood['commentlist'][tempc]['list_3'][templ][0]['pic']['b_url']
                            mood_item['commre'+str(tempc)+str(templ)]=mood['commentlist'][tempc]['list_3'][templ]['content']#楼中楼内容try:
                            mood_item['commrename'+str(tempc)+str(templ)]=mood['commentlist'][tempc]['list_3'][templ]['uin']#楼中楼人
                            mood_item['commtime'+str(tempc)+str(templ)]=mood['commentlist'][tempc]['list_3'][templ]['createTime2']#time
                                      
            temp=0
            tempc=0
            templ=0
            
            with open('result/shtml/'+qqnumber+'/'+self.timen+'.html' if self.inp == '1' else 'result/ahtml/'+self.timen+'/'+qqnumber+'.html','a',encoding='utf-8') as f:
               f.write('<br><br>内容     '+str(em(mood_item['content'])))
               
               for temp in range (0,pictol):
                   
                   try:
                       
                       f.write('<br>pic'+str(temp)+'&nbsp&nbsp<img src="'+str(mood_item['pic'+str(temp)])+'"'+'width=400px;height=400*this.height/this.width'+'>')                             
                   except:
                               break
               if video:
                       try:
                               f.write("<br><video src=\""+mood_item['video']+"\" controls=\"controls\"></video>")
                       except:
                                pass
               f.write('<br>精确时间&nbsp&nbsp '+str(mood_item['created_time'])+'<br>相对时间&nbsp&nbsp'+str(mood_item['createTime'])+'<br>评论数     '+str(mood_item['com_num']))
               f.write('<br>设备名&nbsp&nbsp'+str(mood_item['phone'])+'<br>累计转发&nbsp'+str(mood_item['rt']))
               if mood_item['locate']!='':
                   f.write('<br>位置名称&nbsp'+str(mood_item['locate']))
               if mood_item['loc_pos_x']!='' or mood_item['loc_pos_y']!='':
                   f.write('<br>维度     '+str(mood_item['loc_pos_x'])+'<br>经度     '+str(mood_item['loc_pos_y']))
               for tempc in range(0,mood['cmtnum']):
                    try:
                        
                        lenlis=len(mood['commentlist'][tempc]['list_3'])#楼中楼num
                    except:
                        lenlis=None
                    try:
                        
                        f.write('<br><br>')
                        #head pic
                        f.write('<img src=http://qlogo1.store.qq.com/qzone/'+str(mood_item['commuin'+str(tempc)])+'/'+str(mood_item['commuin'+str(tempc)])+'/30>'+str(mood_item['commuin'+str(tempc)]))
                        
                        f.write('<br>'+'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'+str(em(mood_item['comm'+str(tempc)])))
                        if 'pic' in mood['commentlist'][tempc]:
                                
                                f.write('<img src='+mood['commentlist'][tempc]['pic'][0]['hd_url']+'" width=200px;height=200*this.height/this.width'+'>')
                        f.write('<br>&nbsp&nbsp时间'+str(mood_item['commt'+str(tempc)]))
                    except:
                        
                        pass
                    try:
                        for templ in range (0,lenlis):
                            f.write('<br>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<img src=http://qlogo1.store.qq.com/qzone/'+str(mood_item['commrename'+str(tempc)+str(templ)])+'/'+str(mood_item['commrename'+str(tempc)+str(templ)])+'/30>')
                            f.write('&nbsp&nbsp'+str(mood_item['commrename'+str(tempc)+str(templ)]))#楼中楼人
                            
                            
                            f.write('<br>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'+str(em(mood_item['commre'+str(tempc)+str(templ)])))#楼中楼内容
                            if not mood_item['rerepic']==None:
                                f.write('<img src='+mood_item['rerepic']+'" width=200px;height=200*this.height/this.width'+'>')
                            f.write('<br>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp评论时间'+str(mood_item['commtime'+str(tempc)+str(templ)]))
                    except:
                       pass
               f.write('<br>---------------------------分隔线---------------------------<br>')
               self.poscount+=1
            self.countt += 1
            print('正在处理，计数君报数为： '+str(self.countt))
            #print(self.year,self.count)
            #return (self.year,self.count)

def time1(qq,year,count):
        a="'"
        util.check_path('report/'+str(qq)+'/')
        try :
                os.remove('report/'+str(qq)+'/time1.html')
        except:
                pass
        #shutil.copy('dontmove/echarts.js','report/'+str(qq)+'/')
        shutil.copyfileobj(open('dontmove/time1.part1','r'),open('report/'+str(qq)+'/time1.html','a',encoding='utf-8'))
        with open ('report/'+str(qq)+'/time1.html','a',encoding='utf-8')as f:
                
                f.write(str(year))
        
        shutil.copyfileobj(open('dontmove/time1.part2','r'),open('report/'+str(qq)+'/time1.html','a',encoding='utf-8'))
        with open ('report/'+str(qq)+'/time1.html','a',encoding='utf-8')as f:
                f.write(str(count))
        shutil.copyfileobj(open('dontmove/time1.part3','r'),open('report/'+str(qq)+'/time1.html','a',encoding='utf-8'))
        with open ('report/'+str(qq)+'/time1.html','a',encoding='utf-8')as f:
                for i in range(0,len(year)):
                        f.write('{name:'+a+str(year[i])+a+',value:'+str(count[i])+'}')
                        if i != len(year)-1:
                                f.write(',')
        shutil.copyfileobj(open('dontmove/time1.part4','r'),open('report/'+str(qq)+'/time1.html','a',encoding='utf-8'))
        #print ('ok')
def time2(qq,y,t):
        util.check_path('report/'+str(qq)+'/')
        try :
                os.remove('report/'+str(qq)+'/time2.html')
        except:
                pass
        shutil.copyfileobj(open('dontmove/time2.part1','r'),open('report/'+str(qq)+'/time2.html','a',encoding='utf-8'))
        with open ('report/'+str(qq)+'/time2.html','a',encoding='utf-8')as f:
                
                f.write(str(y))
        shutil.copyfileobj(open('dontmove/time2.part2','r'),open('report/'+str(qq)+'/time2.html','a',encoding='utf-8'))

        
        for i in range(0,len(y)):
                
                
                shutil.copyfileobj(open('dontmove/time2.part3','r'),open('report/'+str(qq)+'/time2.html','a',encoding='utf-8'))
              
                with open ('report/'+str(qq)+'/time2.html','a',encoding='utf-8')as f:
                
                        f.write("'"+str(y[i])+"',")
               
                shutil.copyfileobj(open('dontmove/time2.part4','r'),open('report/'+str(qq)+'/time2.html','a',encoding='utf-8'))
              
                with open ('report/'+str(qq)+'/time2.html','a',encoding='utf-8')as f:
                        
                        f.write(str(t[i]))
                      
                shutil.copyfileobj(open('dontmove/time2.part5','r'),open('report/'+str(qq)+'/time2.html','a',encoding='utf-8'))
                

        
        shutil.copyfileobj(open('dontmove/time2.part6','r'),open('report/'+str(qq)+'/time2.html','a',encoding='utf-8'))



def stime(a):
        b=time.ctime(a)
        b=str(b)
        re=b[-4:]+'年'
        te=b[4:]
        e=te[:3]
        #print (e)
        if e=='Jan':
                re=re+'1月'
        elif e=='Feb':
                re=re+'2月'
        elif e=='Mar':
                re=re+'3月'
        elif e=='Apr':
                re=re+'4月'
        elif e=='May':
                re=re+'5月'
        elif e=='Jun':
                re=re+'6月'
        elif e=='Jul':
                re=re+'7月'
        elif e=='Aug':
                re=re+'8月'
        elif e=='Sep':
                re=re+'9月'
        elif e=='Oct':
                re=re+'10月'
        elif e=='Nov':
                re=re+'11月'
        elif e=='Dec':
                re=re+'12月'
        #print(te)
        te=te[:-5]
        re=re+str(te[4:-9])+'日'
        #print(te)
        te=te[-8:]
        
        
        rea=[]
        rea.append(re+' '+te)
        re=re.replace('年','/')
        re=re.replace('月','/')
        re=re.replace('日','')
        rea.append(re[:4])
        re=re[5:]
        rea.append(re)
        rea.append(te[:-3])
        return rea
#-----------------------------------main------------------------------------
def main():
        year=[]
        count=[]
        inp=input('\n......\n1：整理单人\n2：整理所有人\n')
        if inp=='1':
                tim=input('\n输入...id\n')
                tim=str(tim)            #tim UIN
        dat=input('\n......\n1：整理今天的\n2：整理以前的【输入文件夹名】\n')
        while(len(dat)!=10 and dat!='1'):
                dat=input('\n输入日期有错误 请复制文件夹名！\n')
        if dat=='1':
                dat=timen
                
        dat=str(dat)
        if inp == '1':
                if not os.path.exists('s/'+dat+'/'+tim):
                        if os.path.exists('al/'+dat+'/'+tim+'/'):
                                print('请等待')
                                #util.check_path()
                                shutil.copytree('al/'+dat+'/'+tim+'/','s/'+dat+'/'+tim)
                        else:
                                print('未找到文件夹 请先获取')
                                
        
        if inp=='1':#单人
                pos = 0
                app = Get_detail(inp,dat)
                mood_dict = app.make_dict(1,tim,dat)
                if not os.path.exists('result/shtml/'+tim+'/'):
                        os.mkdir('result/shtml/'+tim+'/')
                try:
                        os.remove('result/'+'shtml/'+tim+'/'+dat+'.html')
                except:
                        pass
                with open('result/'+'shtml/'+tim+'/'+dat+'.html','a',encoding='utf-8') as f:
                        f.write('<body>')
                
                
                f='s/'+dat+'/'+tim+'/'
         
                for dirname, fname in mood_dict.items():
                        for each_file in fname:
                                filename=str(f)+str(pos)
                                if not os.path.exists(filename):
                                        
                                        break
                                
                                app.exact_mood_data(tim,filename)
                                

                                year=app.year
                                count=app.count
                                print(pos,app.poscount)
                                pos+=20#2018.10.3更新 说说将按时间顺序排布
                #print(app.t)
                print('正在处理数据...')
                for s in range(0,len(app.t)):
                        for m in range(0,len(app.t[s])):
                                app.t[s][m][0]=app.tyear[s]+'/'+app.t[s][m][0]
                time1(str(tim),year,count)
                time2(str(tim),app.tyear,app.t)
                
                
                
                
        else:
                if not os.path.exists('result/ahtml/'+dat+'/'):
                        os.mkdir('result/ahtml/'+dat+'/')
                pos = 0
                app = Get_detail(None,dat)
                mood_dict = app.make_dict(0,None,dat)
                for dirname, fname in mood_dict.items():
                        yera=[]
                        count=[]
                        tt=[]
                        try:
                                os.remove('result/'+'ahtml/'+dat+'/'+dirname+'.html')
                        except:
                                pass
                        with open('result/'+'ahtml/'+dat+'/'+dirname+'.html','a',encoding='utf-8') as f:
                                f.write('<head><meta charset = "UTF-8"><title>'+dirname+'</title>'+'</head><body>')
                        for each_file in fname:
                                filename = os.path.join('al',dat,dirname,str(pos))
                                app.exact_mood_data(dirname, filename)
                                year=app.year
                                count=app.count
                                pos+=20
                        with open('result/ahtml/'+dat+'/'+dirname+'.html','a',encoding='utf-8') as f:
                                f.write('</body>')
                        for s in range(0,len(app.t)):
                                for m in range(0,len(app.t[s])):
                                        app.t[s][m][0]=app.tyear[s]+'/'+app.t[s][m][0]
                        time1(str(dirname),year,count)
                        time2(str(dirname),app.tyear,app.t)
                        print(dirname+' 已完成')
                        pos=0
                        app=Get_detail(inp,dat)
        print('整理完成!')

def ddd(b):
        year=[]
        count=[]
        inp='1'
        if inp=='1':
                tim=str(b)
                           #tim UIN
        dat='1'
        if dat=='1':
                dat=timen
                
        dat=str(dat)
        if inp == '1':
                if not os.path.exists('s/'+dat+'/'+tim):
                        if os.path.exists('al/'+dat+'/'+tim+'/'):
                                print('请等待')
                                #util.check_path()
                                shutil.copytree('al/'+dat+'/'+tim+'/','s/'+dat+'/'+tim)
                        else:
                                print('未找到文件夹 请先获取')
                                
        
        if inp=='1':#单人
                pos = 0
                app = Get_detail(inp,dat)
                mood_dict = app.make_dict(1,tim,dat)
                if not os.path.exists('result/shtml/'+tim+'/'):
                        os.mkdir('result/shtml/'+tim+'/')
                try:
                        os.remove('result/'+'shtml/'+tim+'/'+dat+'.html')
                except:
                        pass
                with open('result/'+'shtml/'+tim+'/'+dat+'.html','a',encoding='utf-8') as f:
                        f.write('<body>')
                
                
                f='s/'+dat+'/'+tim+'/'
         
                for dirname, fname in mood_dict.items():
                        for each_file in fname:
                                filename=str(f)+str(pos)
                                if not os.path.exists(filename):
                                        
                                        break
                                
                                app.exact_mood_data(tim,filename)

                                year=app.year
                                count=app.count
                                
                                pos+=20#2018.10.3更新 说说将按时间顺序排布
                #print(app.t)
                print('正在处理数据...')
                for s in range(0,len(app.t)):
                        for m in range(0,len(app.t[s])):
                                app.t[s][m][0]=app.tyear[s]+'/'+app.t[s][m][0]
                time1(str(tim),year,count)
                time2(str(tim),app.tyear,app.t)

#-----------------------------------/main------------------------------------



        
if __name__=='__main__':
        main()
