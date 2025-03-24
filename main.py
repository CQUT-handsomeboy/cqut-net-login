import requests
import re

from dotenv import load_dotenv
from encrypt import *
from icecream import ic
from json import load
from urllib.parse import quote, parse_qs, urlparse

load_dotenv()

with open(".env.json", "r", encoding="utf-8") as f:
    data: dict = load(f)
    ACCOUNT = data.get("account")
    PASSWORD = data.get("password")
    PASSWORD_ENCRYPTED = data.get("passwordEncrypted")
    SERVICE = data.get("service")

# 获取JSESSIONID
url = "http://202.202.145.132"

headers3 = {
    "Accept-Language": "zh-CN",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Host": "202.202.145.132",
}

response = requests.get(url, headers=headers3, allow_redirects=False)  # 禁止重定向
JSESSIONID = list(response.cookies)[0].value

ic(JSESSIONID)

if response.status_code == 302:
    target = response.headers["Location"]
    response = requests.get(target, headers=headers3)
else:
    ic("状态码出错")
    exit(0)

pattern = r"top\.self\.location\.href='([^']*)'"
match = re.search(pattern, response.text)
href_value = match.group(1)
queryString = href_value.split("?")[1]

ic(queryString)

url = "https://uis.cqut.edu.cn/center-auth-server/vbZl4061/cas/login?service=https://sid.cqut.edu.cn/cas/login?client_name=adapter"

headers1 = {
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

response = requests.get(url, headers=headers1)

cookies = response.cookies

url = "https://uis.cqut.edu.cn/center-auth-server/sso/doLogin"

headers2 = {
    "Host": "uis.cqut.edu.cn",
    "Content-Type": "application/json, application/json;charset=UTF-8",
    "Accept": "*/*",
    "Origin": "https://uis.cqut.edu.cn",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://uis.cqut.edu.cn/center-auth-server/vbZl4061/cas/login?service=https://sid.cqut.edu.cn/cas/login?client_name=adapter",
} | headers1

public_key_pem = """-----BEGIN PUBLIC KEY-----
    MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDACwPDxYycdCiNeblZa9LjvDzb
    iZU1vc9gKRcG/pGjZ/DJkI4HmoUE2r/o6SfB5az3s+H5JDzmOMVQ63hD7LZQGR4k
    3iYWnCg3UpQZkZEtFtXBXsQHjKVJqCiEtK+gtxz4WnriDjf+e/CxJ7OD03e7sy5N
    Y/akVmYNtghKZzz6jwIDAQAB
    -----END PUBLIC KEY-----
    """

data = {
    "name": ACCOUNT,
    "pwd": PASSWORD_ENCRYPTED,
    # "pwd":get_secret_param(PASSWORD, public_key_pem)
    "verifyCode": None,
    "universityId": "100005",
    "loginType": "login",
}

response = requests.post(url, headers=headers2, data=json.dumps(data), cookies=cookies)

ic(response.status_code)
ic(response.text)


# 获取userIndex
url = "http://202.202.145.132/eportal/InterFace.do?method=loginOfCas"

headers4 = {
    "Host": "202.202.145.132",
    "Accept-Language": "zh-CN",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "*/*",
    "Origin": "http://202.202.145.132",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

cookies = {
    "EPORTAL_COOKIE_SERVER": "",
    "EPORTAL_COOKIE_SERVER_NAME": "",
    "servicesJsonStr": quote(f"{ACCOUNT}@%%username@%%中国电信@中国移动@校园内网"),
    "EPORTAL_COOKIE_DOMAIN": "",
    "EPORTAL_COOKIE_OPERATORPWD": "",
    "JSESSIONID": JSESSIONID,  # 需要设置成上述获取到的JSESSIONID
}

data = {
    "userId": ACCOUNT,
    "flag": "casauthofservicecheck",
    # 需要编码两次
    "service": quote(quote(SERVICE)),  # 中国移动 / 中国电信
    # 需要编码两次
    "queryString": quote(quote(queryString)),
    "operatorPwd": "",  # 空
    "operatorUserId": "",  # 空
    "passwordEncrypt": "false",
    "rememberService": "false",
}

response = requests.post(
    "http://202.202.145.132/eportal/InterFace.do?method=loginOfCas",
    headers=headers4,
    data=data,
    cookies=cookies,
)

ic(response.status_code)
ic(response.text)
