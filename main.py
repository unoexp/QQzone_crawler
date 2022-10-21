#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os

import get_moods
import get_moods_detail
import get_my_friends
import get_qq_number
import util


def main():
    print('准备工作')
    util.check_path(os.path.join('friends'))
    util.check_path(os.path.join('content', 'all'))
    util.check_path(os.path.join('content', 'single'))
    util.check_path(os.path.join('report'))
    util.check_path(os.path.join('result'))
    util.check_path(os.path.join('result', 'all_html'))
    util.check_path(os.path.join('result', 'single_html'))

    get_qq_item_obj = get_qq_number
    get_qq_item_obj.exact_qq_number()
    print('欢迎使用！')
    a = input('输入...\n1：收集所有人（同时重新获取好友列表）\n2：收集所有人（不重新获取好友列表）\n3：获取单人\n')
    while True:
        if a == '1':  # 所有人 同时重新获取好友列表
            get_friends_obj = get_my_friends.Get_friends_number()
            get_friends_obj.get_friends()
            get_qq_item_obj = get_qq_number
            get_qq_item_obj.exact_qq_number()
            get_moods_obj = get_moods.Get_moods_start(0)
            get_moods_obj.get_moods_start(0)
            print('\n收集完成！ 正在自动整理...\n')
            get_moods_detail.main(2)
            break
        elif a == '2':  # 所有人 不重新获取好友列表
            get_qq_item_obj = get_qq_number
            get_qq_item_obj.exact_qq_number()
            get_moods_obj = get_moods.Get_moods_start(0)
            get_moods_obj.get_moods_start(0)
            print('\n收集完成！ 正在自动整理...\n')
            get_moods_detail.main(2)
            break
        elif a == '3':  # 单人
            b = input('\n请输入qq号码: ')
            get_moods_obj = get_moods.Get_moods_start(str(b))
            get_moods_obj.get_moods_start(1)
            print('\n收集完成！ 正在自动整理...\n')
            get_moods_detail.main(1, str(b))
            break
        else:
            a = input('输入错误, 请重新输入')
    print('如有需要可运行get_moods_detail.py单独整理某人/某天的')


if __name__ == '__main__':
    main()
