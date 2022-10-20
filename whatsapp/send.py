import os
from drivers.get_draver import get
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
from loguru import logger
from whatsapp import login
from selenium.webdriver.common.keys import Keys
from whatsapp.config import finding_delay


def send_message(phone, text):
    dir_path = os.getcwd()
    profile = os.path.join(dir_path, "profile", "wpp")
    options = webdriver.ChromeOptions()
    options.add_argument(r"user-data-dir={}".format(profile))
    driver = get(options)
    result = login.login(driver)
    if not result:
        return False
    phone = str(phone)
    if phone[0] == '8':
        phone[0] = '7'
    if phone[0] == '+':
        phone = phone[1:]
    driver.get(f"https://web.whatsapp.com/send/?phone={phone}")
    element = driver.find_element(By.ID, "app")
    count = 0
    while True:
        if count * 5 >= finding_delay:
            logger.error('Не могу найти контакт, поменяйте номер или увеличьте задержку')
            return False
        try:
            element = element.find_element(By.CLASS_NAME, "_3xTHG")
            break
        except Exception as e:
            sleep(5)
            count += 1

    element = element.find_element(By.CLASS_NAME, "_2cYbV")
    element = element.find_element(By.CLASS_NAME, "_2BU3P")
    element = element.find_element(By.CLASS_NAME, "_1SEwr")
    element = element.find_element(By.CLASS_NAME, "_6h3Ps")
    element = element.find_element(By.CLASS_NAME, "_2lMWa")
    element = element.find_element(By.CLASS_NAME, "p3_M1")
    element = element.find_element(By.CLASS_NAME, "g0rxnol2")

    cliked = element.find_element(By.CLASS_NAME, "fd365im1").click()
    element = element.find_element(By.CLASS_NAME, "fd365im1")
    element.send_keys(str(text))
    element.send_keys(Keys.ENTER)
    sleep(5)
    return True
