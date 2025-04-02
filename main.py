import requests
import re
import inspect

from icecream import ic
from json import load, dumps
from urllib.parse import quote, parse_qsl, urlparse
from rich import print


with open(".env.json", "r", encoding="utf-8") as f:
    data: dict = load(f)
    ACCOUNT = data.get("account")
    PASSWORD = data.get("password")
    PASSWORD_ENCRYPTED = data.get("passwordEncrypted")
    SERVICE = data.get("service")


def function_log(func):

    def wrapper(*args, **kwargs):
        ps = list(inspect.signature(func).parameters)
        print(f"{func.__name__} [blue]开始执行,参数列表{ps}[/blue]")
        result = func(*args, **kwargs)
        print(f"{func.__name__} 执行结果:[green]{result}[/green]")
        print("-" * 10)
        return result

    return wrapper


@function_log
def get_JSESSIONID_and_next_location():
    headers = {
        "Accept-Language": "zh-CN",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Host": "202.202.145.132",
    }
    url = "http://202.202.145.132"
    response = requests.get(url, headers=headers, allow_redirects=False)
    JSESSIONID = list(response.cookies)[0].value
    next_location = response.headers["Location"]
    return JSESSIONID, next_location


@function_log
def get_js_tag_href_value(JSESSIONID, next_location):
    headers = {
        "Accept-Language": "zh-CN",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Host": "202.202.145.132",
    }
    cookies = {
        "EPORTAL_COOKIE_SERVER": "",
        "EPORTAL_COOKIE_SERVER_NAME": "",
        "JSESSIONID": JSESSIONID,
    }
    response = requests.get(next_location, headers=headers, cookies=cookies)
    pattern = r"top\.self\.location\.href='([^']*)'"
    match = re.search(pattern, response.text)
    href_value = match.group(1)
    return href_value


@function_log
def get_SESSION_and_refer_url(JSESSIONID, js_tag_href):
    headers = {
        "Accept-Language": "zh-CN",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Host": "202.202.145.132",
    }
    cookies = {
        "EPORTAL_COOKIE_SERVER": "",
        "EPORTAL_COOKIE_SERVER_NAME": "",
        "JSESSIONID": JSESSIONID,
    }
    response = requests.get(
        js_tag_href, headers=headers, cookies=cookies, allow_redirects=False
    )
    next_location = response.headers["Location"]

    response = requests.get(
        next_location,
        headers=headers
        | {"Host": "sid.cqut.edu.cn", "Refer": "http://123.123.123.123/"},
    )

    print(f"[purple]{response.status_code}[/purple]")
    print(f"[purple]{response.text}[/purple]")

    SESSION = list(response.cookies)[0].value
    refer_url = response.url

    return SESSION, refer_url


@function_log
def get_PAC4JDELSESSION_and_next_location(SESSION, refer_url, href_value):
    headers = {
        "Host": "sid.cqut.edu.cn",
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
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=0, i",
        "Connection": "keep-alive",
    }

    print("refer_url", refer_url)

    response = requests.get(
        # url="http://127.0.0.1:8765/cas/clientredirect?client_name=adapter",
        url="http://sid.cqut.edu.cn/cas/clientredirect?client_name=adapter",
        headers=headers,
        cookies={"SESSION": SESSION},
        params={"service": href_value},
        allow_redirects=False,
    )

    assert response.status_code == 308, str(response.status_code)
    next_location = response.headers["Location"]

    headers = {
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
        "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Accept-Language": "zh-CN",
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=0, i",
        "Connection": "keep-alive",
        "Referer": refer_url,
    }

    response = requests.get(next_location, headers=headers, allow_redirects=False)
    print(
        response.cookies
    )  # 这里的cookies有设置新的SESSION，此时JSESSIONID失效，疑惑？

    return


if __name__ == "__main__":
    JSESSIONID, next_location = get_JSESSIONID_and_next_location()
    href_value = get_js_tag_href_value(JSESSIONID, next_location)
    queryString = href_value.split("?")[1]
    SESSION, refer_url = get_SESSION_and_refer_url(JSESSIONID, href_value)
    get_PAC4JDELSESSION_and_next_location(SESSION, refer_url, href_value)
    exit(0)
