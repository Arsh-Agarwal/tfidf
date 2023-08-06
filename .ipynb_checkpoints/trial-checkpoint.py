import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


service = Service('chromedriver.exe')
driver = webdriver.Chrome(service=service)
heading_class = "mr-2 text-label-1"
body_class = "_1l1MA"

def getLCPageData(url, index):
    try:
        driver.get(url)
        time.sleep(7)
        #heading = driver.find_element(By.CSS_SELECTOR, heading_class)
        body = driver.find_element(By.CSS_SELECTOR, body_class)
        #print(heading.text)
        print(body.text)
        return True
    except Exception as e:
        print(e)
        return False

links = []
with open('leetcode.txt', 'r') as file:
    for line in file:
        if line!='\n': links.append(line)
getLCPageData(links[0], 1)