import requests
import re
import json

from urllib.parse import urlparse, parse_qs, quote

with open(".env.json", "r", encoding="utf-8") as f:
    meta = json.load(f)
    ACCOUNT = meta["account"]
    PASSWORD = meta["password"]
    PASSWORD_ENCRYPTED = meta["passwordEncrypted"]
    SERVICE = meta["service"]  # 需要登录的运营商名称 中国移动/中国电信

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

print("service", service)
print("queryString", queryString)

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
print("SESSION", SESSION is not None)

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

print("PAC4JDELSESSION", PAC4JDELSESSION is not None)
print("COOKIE_AUTH_SERVER_CLIENT_TAG", COOKIE_AUTH_SERVER_CLIENT_TAG is not None)

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
    "pwd": PASSWORD_ENCRYPTED,
    "universityId": "100005",
    "verifyCode": None,
}

res = session.post(burp0_url, headers=burp0_headers, json=burp0_json)  # 034


auth_server_token = session.cookies.get("auth_server_token")
COOKIE_AUTH_SERVER_CLIENT_TAG_SURVIVAL_TOKEN = session.cookies.get(
    "COOKIE_AUTH_SERVER_CLIENT_TAG_SURVIVAL_TOKEN"
)

print("auth_server_token", auth_server_token is not None)
print(
    "COOKIE_AUTH_SERVER_CLIENT_TAG_SURVIVAL_TOKEN",
    COOKIE_AUTH_SERVER_CLIENT_TAG_SURVIVAL_TOKEN is not None,
)

print(res.json())  # 登陆成功

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

print(res.status_code)

PAC4JDELSESSION = session.cookies.get("PAC4JDELSESSION")
SOURCEID_TGC = session.cookies.get("SOURCEID_TGC")
rg_objectid = session.cookies.get("rg_objectid")

print("PAC4JDELSESSION", PAC4JDELSESSION)
print("SOURCEID_TGC", SOURCEID_TGC)
print("rg_objectid", rg_objectid)

# loginOfCas

burp0_url = "http://202.202.145.132:80/eportal/InterFace.do?method=loginOfCas"

burp0_cookies = {
    "EPORTAL_COOKIE_SERVER": "",
    "EPORTAL_COOKIE_SERVER_NAME": "",
    "servicesJsonStr": f"{ACCOUNT}%40%25%25username%40%25%25%E4%B8%AD%E5%9B%BD%E7%94%B5%E4%BF%A1%40%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8%40%E6%A0%A1%E5%9B%AD%E5%86%85%E7%BD%91",
    # 手动，JS设置
    "EPORTAL_COOKIE_DOMAIN": "",
    "EPORTAL_COOKIE_OPERATORPWD": "",
    "JSESSIONID": session.cookies["JSESSIONID"],
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

print(res.status_code)

userIndex = res.json()["userIndex"]
print("userIndex", userIndex)


print("登陆成功!")
