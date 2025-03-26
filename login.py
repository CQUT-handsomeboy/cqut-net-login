from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from json import load
from icecream import ic
from time import sleep

with open("./.env.json", "r", encoding="utf-8") as f:
    data = load(f)
    chrome_driver_path = data.get("chromeDriverPath")
    ACCOUNT = data.get("account")
    PASSWORD = data.get("password")

assert chrome_driver_path is not None, "设置 chromeDriverPath"

service = Service(chrome_driver_path)

chrome_options = Options()

# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(service=service, options=chrome_options)

driver.execute_cdp_cmd(
    "Page.addScriptToEvaluateOnNewDocument",
    {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
            """
    },
)

driver.get(
    "https://uis.cqut.edu.cn/center-auth-server/vbZl4061/cas/login?service=https%3A%2F%2Fsid.cqut.edu.cn%2Fcas%2Flogin%3Fclient_name%3Dadapter"
)

account_input = driver.find_element(
    By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div[2]/form/div[1]/div/div/input'
)
account_input.send_keys(ACCOUNT)

password_input = driver.find_element(
    By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div[2]/form/div[2]/div/div/input'
)
password_input.send_keys(PASSWORD)

driver.save_screenshot("input_account_and_password.png")

sleep(3)

login_button = driver.find_element(
    By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div[2]/button'
)
login_button.click()

# 会显示登陆异常（有检测），导致后续无法进行运营商选择，至今无法解决

WebDriverWait(driver, 30).until(
    EC.presence_of_all_elements_located((By.ID, "loginLink_div"))
)

service0_selected = driver.find_element(By.ID, "_service_0")
service0_selected.click()
ic(service0_selected.text)

service1_selected = driver.find_element(By.ID, "_service_1")
service1_selected.click()
ic(service1_selected.text)

driver.save_screenshot("login_and_choose_service.png")

driver.quit()
