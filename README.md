# QQzone_crawler
QQ 空间动态爬虫, 利用cookie登录获取所有可访问好友空间的动态并保存到本地

需要先安装第三方库 **requests** <br />

[点击这里下载代码](https://github.com/unoexp/QQzone_crawler/archive/refs/heads/master.zip)

# 各程序文件说明

**main.py**： 程序主入口, 运行时执行`python main.py`即可

**get_my_friends.py**： 用于从QQ空间服务器获取包括自己的QQ好友信息的文件, 其中包括他们的QQ号和名称（此处是备注名），保存到本地，每个文件中保存有50个

**get_qq_number.py**： 用于从上一步保存好的文件中提取出所有好友的QQ号和名称, QQ号和名称以字典形式保存, 再以它们组成的字典为作元素构造列表, 再保存到本地, 文件名为qqnumber.inc

**get_moods.py**： 用于从QQ空间服务器获取包含每个好友空间发表的说说的文件, 其中包含每个说说的发表时间, 内容(包括图片与视频), 评论, 评论的评论, 地点信息, 手机信息等

**cookie_file**： 用于放置自己登录QQ空间后得到的cookie. 从浏览器中复制出来放在这个文件内即可, 在负责处理cookie的函数中有对应的处理代码来处理换行符, 但还是希望不要出现多行, 末尾也不要有多余的空行. **但要注意的是, 这个文件里面只能放一个cookie. 它的作用是方便设置cookie, 而不是用于反反爬虫.** 如果不知道怎么获取cookie, 请看[这里](http://www.xjr7670.com/articles/how-to-get-qzone-cookie.html)

---

# 可视化部分

**get_moods_detail.py**：程序在执行完 get_moods.py 中的功能之后, 会把包含有每个好友的说说文件保存到本地. 而这个程序就是用于把说说信息从这些文件里面提取出来, 执行程序后会生成三个文件, 分别位于result文件夹和report文件夹内, result内的文件为好友说说的html文件, 其中包括已经简单排版的所有说说内容. report文件夹内包含time1和time2文件, 分别为好友年度发布次数统计图和日度发布次数统计图.

## 注意事项

1. **获取QQ好友信息是间接获取的。需要先在QQ空间中将自己空间的访问权限先设置为仅QQ好友可访问。然后程序才能够正常运行**

2. **main程序运行成功后会自动对爬取的数据进行一次整理**
