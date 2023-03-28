from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from urllib.parse import urljoin
import ddddocr
from time import sleep
import os
import re

info = os.popen("phpstudy -instinfo").read()

url = re.search("http://127.0.0.1:9080/[0-9a-zA-Z]{6}", info).group(0)
password = re.search("[0-9a-zA-Z]{10}", info).group(0)


options = webdriver.FirefoxOptions()
options.add_argument('--headless')
browser = webdriver.Firefox(executable_path="/robot/geckodriver", options=options)
browser.get(url)
sleep(3)
browser.find_element(By.ID, "username").send_keys("admin")
browser.find_element(By.ID, "password").send_keys(password)


captcha = browser.find_element(By.ID, "captcha")
data = captcha.screenshot_as_png
ocr = ddddocr.DdddOcr()

browser.find_element(By.ID, "verifycode").send_keys(ocr.classification(data))

button = browser.find_element(By.XPATH, '//*[@id="LAY_app"]/div/div/div/div[5]/div/button')
button.click()
while True:
    sleep(60)
    browser.refresh()