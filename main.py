#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import get_my_friends
import get_moods
import get_qq_number
import get_moods_detail
import requests
def main():
    print('准备工作')
    get_qq_item_obj = get_qq_number.exact_data_from_result()
    get_qq_item_obj.exact_qq_number()
    print('欢迎！')
    a=input('\n输入...\n1：收集所有人（并重新获取好友列表）\n2：收集所有人（不重新获取好友列表）\n3：获取单人\n')
    while(True):
        
        if a=='1':#所有人 with friends
            get_friends_obj = get_my_friends.Get_friends_number()
            get_friends_obj.get_friends()
            get_qq_item_obj = get_qq_number.exact_data_from_result()
            get_qq_item_obj.exact_qq_number()
            get_moods_obj = get_moods.Get_moods_start(0)
            get_moods_obj.get_moods_start(0)
            break
        elif a=='2':#所有人 without friends
            get_qq_item_obj = get_qq_number.exact_data_from_result()
            get_qq_item_obj.exact_qq_number()
            get_moods_obj = get_moods.Get_moods_start(0)
            get_moods_obj.get_moods_start(0)
            break
        elif a=='3':#单人
            b= input('\n输入id\n')
            get_moods_obj=get_moods.Get_moods_start(str(b))
            get_moods_obj.get_moods_start(1)
            break
        elif a=='4': 
#            将number替换为自定义号码            
            gt('number') #输入自定义号码
            #gt('...')
            
            print('收集完成')
            return
        elif a=='0': 
            gt('number')#自定义
            return
        elif a=='.':
            com('number')
        else:
            a=input('你输'+str(a)+'干什么呢？？\n重新输')
            
    c= input('\n收集完成！\n\n是否整理？\n1：整理\n2：不整理\n')
    if c == '1':
        paa=get_moods_detail.main()
    else:
        print('如果想单独整理可运行get_moods_detail.py')
        
def gt(num):
    get_moods_obj=get_moods.Get_moods_start(num)
    get_moods_obj.get_moods_start(1)
    paa=get_moods_detail.ddd(num)
def com(num):
    ge=get_moods.Get_moods(num)
    ge.compare()
main()
