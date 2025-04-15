import requests
import re

from urllib.parse import urlparse, parse_qs, quote
from encrypt import getSecretParam
from tkinter import messagebox
from os import getenv
from dotenv import load_dotenv

load_dotenv()

ACCOUNT = getenv("cqut_account")
PASSWORD = getenv("cqut_password")
SERVICE = getenv("cqut_net_service")

assert ACCOUNT is not None
assert PASSWORD is not None
assert SERVICE in {"中国移动", "中国电信"}

session = requests.session()

burp0_url = "http://202.202.145.132:80/"

burp0_headers = {
    "Accept-Language": "zh-CN",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

res = session.get(burp0_url, headers=burp0_headers)  # 001

pattern = r"top\.self\.location\.href='([^']*)'"
match = re.search(pattern, res.text)
service = match.group(1)
_, queryString = service.split("?", maxsplit=1)

burp0_headers = {
    "Accept-Language": "zh-CN",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Referer": "http://123.123.123.123/",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

res = session.get(service, headers=burp0_headers)  # 004
refer_url = res.url

SESSION = session.cookies.get("SESSION")
assert SESSION is not None, "获取SESSION失败"

burp0_url = "https://sid.cqut.edu.cn/cas/clientredirect"

burp0_headers = {
    "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Accept-Language": "zh-CN",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Dest": "document",
    "Referer": refer_url,
    "Priority": "u=0, i",
    "Connection": "keep-alive",
}

params = {
    "client_name": ["adapter"],
    "service": [service],
}

res = session.get(burp0_url, headers=burp0_headers, params=params)  # 007 -> 011
refer_url = res.url

service_with_delegatedclientid = parse_qs(urlparse(refer_url).query).get("service")

PAC4JDELSESSION = session.cookies.get("PAC4JDELSESSION")
COOKIE_AUTH_SERVER_CLIENT_TAG = session.cookies.get("COOKIE_AUTH_SERVER_CLIENT_TAG")

assert PAC4JDELSESSION is not None, "获取PAC4JDELSESSION失败"
assert (
    COOKIE_AUTH_SERVER_CLIENT_TAG is not None
), "获取COOKIE_AUTH_SERVER_CLIENT_TAG失败"

# 登录
burp0_url = "https://uis.cqut.edu.cn:443/center-auth-server/sso/doLogin"
burp0_headers = {
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
    "Referer": refer_url,
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=1, i",
}

burp0_json = {
    "loginType": "login",
    "name": ACCOUNT,
    "pwd": getSecretParam(PASSWORD),
    # "pwd": PASSWORD_ENCRYPTED,
    "universityId": "100005",
    "verifyCode": None,
}

res = session.post(burp0_url, headers=burp0_headers, json=burp0_json)  # 034

auth_server_token = session.cookies.get("auth_server_token")
COOKIE_AUTH_SERVER_CLIENT_TAG_SURVIVAL_TOKEN = session.cookies.get(
    "COOKIE_AUTH_SERVER_CLIENT_TAG_SURVIVAL_TOKEN"
)

doLogin_json: dict = res.json()

assert (
    isinstance(doLogin_json, dict)
    and doLogin_json["code"] == 200
    and "登录成功" in doLogin_json["msg"].strip()
), "登陆失败，可能账号或者密码错误"

assert auth_server_token is not None, "获取auth_server_token失败"
assert (
    COOKIE_AUTH_SERVER_CLIENT_TAG_SURVIVAL_TOKEN is not None
), "获取COOKIE_AUTH_SERVER_CLIENT_TAG_SURVIVAL_TOKEN失败"


burp0_url = "https://uis.cqut.edu.cn:443/center-auth-server/vbZl4061/cas/login"

burp0_headers = {
    "Cache-Control": "max-age=0",
    "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Accept-Language": "zh-CN",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": refer_url,
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=0, i",
}

params = {"service": [service_with_delegatedclientid]}

cookies = {
    "COOKIE_AUTH_SERVER_CLIENT_TAG": session.cookies["COOKIE_AUTH_SERVER_CLIENT_TAG"],
    "auth_server_token": session.cookies["auth_server_token"],
    "COOKIE_AUTH_SERVER_CLIENT_TAG_SURVIVAL_TOKEN": session.cookies[
        "COOKIE_AUTH_SERVER_CLIENT_TAG_SURVIVAL_TOKEN"
    ],
}

res = session.get(
    burp0_url,
    headers=burp0_headers,
    params=params,
    cookies=cookies,
)  # 035

PAC4JDELSESSION = session.cookies.get("PAC4JDELSESSION")
SOURCEID_TGC = session.cookies.get("SOURCEID_TGC")
rg_objectid = session.cookies.get("rg_objectid")

assert PAC4JDELSESSION is None, "获取PAC4JDELSESSION失败"
assert SOURCEID_TGC is not None, "获取SOURCEID_TGC失败"
assert rg_objectid is not None, "获取rg_objectid失败"

# loginOfCas

burp0_url = "http://202.202.145.132:80/eportal/InterFace.do?method=loginOfCas"

JSESSIONID = session.cookies.get("JSESSIONID")
assert JSESSIONID is not None, "获取JSESSIONID失败"

burp0_cookies = {
    "EPORTAL_COOKIE_SERVER": "",
    "EPORTAL_COOKIE_SERVER_NAME": "",
    "servicesJsonStr": f"{ACCOUNT}%40%25%25username%40%25%25%E4%B8%AD%E5%9B%BD%E7%94%B5%E4%BF%A1%40%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8%40%E6%A0%A1%E5%9B%AD%E5%86%85%E7%BD%91",
    # 手动，JS设置
    "EPORTAL_COOKIE_DOMAIN": "",
    "EPORTAL_COOKIE_OPERATORPWD": "",
    "JSESSIONID": JSESSIONID,
}

burp0_headers = {
    "Accept-Language": "zh-CN",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "*/*",
    "Origin": "http://202.202.145.132",
    "Referer": service,
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

burp0_data = {
    "userId": ACCOUNT,
    "flag": "casauthofservicecheck",
    "service": quote(SERVICE),
    "queryString": queryString,
    "operatorPwd": "",
    "operatorUserId": "",
    "passwordEncrypt": "false",
    "rememberService": "false",
}

res = session.post(
    burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data
)

loginOfCas_json = res.json()

assert (
    isinstance(loginOfCas_json, dict)
    and "获取JSESSIONID失败"
    and loginOfCas_json.get("userIndex")
), "获取userIndex失败"

print("登陆成功!")
messagebox.showinfo("提示", "登录成功！")
