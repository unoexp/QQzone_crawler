import json
import os


def exact_qq_number():
    friendsFiles = [x for x in os.listdir('friends') if x.endswith("json")]

    qqNum_list = []
    i = 0
    for each_file in friendsFiles:
        with open('friends/' + each_file, encoding='utf-8') as f:
            source = f.read()
            con_dict = source[75:-4].replace('\n', '')
            con_json = json.loads(con_dict)
            friends_list = con_json['uinlist']

            for item in friends_list:
                i = i + 1
                qqNum_list.append(item)
    else:
        with open('qqnumber.inc', 'w', encoding='utf-8') as f:
            f.write(str(qqNum_list))

