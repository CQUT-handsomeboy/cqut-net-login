import requests

from termcolor import colored
from dotenv import load_dotenv
from os import getenv
from encrypt import *

load_dotenv()

ACCOUNT = getenv("ACCOUNT")
PASSWORD = getenv("PASSWORD")

import requests

url = "https://uis.cqut.edu.cn/center-auth-server/vbZl4061/cas/login?service=https://sid.cqut.edu.cn/cas/login?client_name=adapter"

headers = {
    "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Accept-Language": "zh-CN",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=0, i",
    "Connection": "keep-alive",
}

response = requests.get(url, headers=headers)

cookies = response.cookies

url = "https://uis.cqut.edu.cn/center-auth-server/sso/doLogin"

headers = {
    "Host": "uis.cqut.edu.cn",
    "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Accept-Language": "zh-CN",
    "Sec-Ch-Ua-Mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
    "Content-Type": "application/json, application/json;charset=UTF-8",
    "Accept": "*/*",
    "Origin": "https://uis.cqut.edu.cn",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://uis.cqut.edu.cn/center-auth-server/vbZl4061/cas/login?service=https://sid.cqut.edu.cn/cas/login?client_name=adapter",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=1, i",
    "Connection": "keep-alive",
}

public_key_pem = """-----BEGIN PUBLIC KEY-----
    MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDACwPDxYycdCiNeblZa9LjvDzb
    iZU1vc9gKRcG/pGjZ/DJkI4HmoUE2r/o6SfB5az3s+H5JDzmOMVQ63hD7LZQGR4k
    3iYWnCg3UpQZkZEtFtXBXsQHjKVJqCiEtK+gtxz4WnriDjf+e/CxJ7OD03e7sy5N
    Y/akVmYNtghKZzz6jwIDAQAB
    -----END PUBLIC KEY-----
    """

data = {
    "name": ACCOUNT,
    "pwd": get_secret_param(PASSWORD,public_key_pem),
    "verifyCode": None,
    "universityId": "100005",
    "loginType": "login",
}

response = requests.post(url, headers=headers, data=json.dumps(data), cookies=cookies)

print(colored(response.status_code, "cyan"))
print(colored(response.text, "green"))
