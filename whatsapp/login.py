from selenium.webdriver.common.by import By
from time import sleep
from loguru import logger
from whatsapp.config import login_delay


def login(driver):
    driver.get("https://web.whatsapp.com/")
    counter = 0
    while True:
        if counter * 5 > login_delay:
            logger.error('Не могу войти в whatsapp')
            return False
        try:
            element = driver.find_element(
                By.ID,
                "app"
            )
            element = element.find_element(
                By.CLASS_NAME,
                '_3Bc7H'
            )
            logger.info('Вы вошли')
            return True
        except Exception as e:
            logger.warning('Вход не выполнен')
            try:
                counter += 1
                qr_description = driver.find_element(
                    By.CLASS_NAME,
                    '_2UwZ_'
                )
                sleep(5)
            except Exception as e:
                logger.warning('Не могу найти qr код для входа')
                sleep(5)
