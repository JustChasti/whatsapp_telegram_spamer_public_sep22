import os
import sys
import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

phone = '89014535343'
#msg = message_text
msg = 'message_text'

DATA_PATH_GOOGLE = os.path.join(os.getcwd(), 'ChromeData', 'GOOGLE')
DRIVER_PATH = os.path.join(os.getcwd(), 'drivers/chrome_win.exe')


class GoogleBot:
    def __init__(self, DATA_PATH_GOOGLE, DRIVER_PATH):
        opts = webdriver.ChromeOptions()
        opts.add_argument(f'user-data-dir={DATA_PATH_GOOGLE}')
        opts.add_argument('--disable-gpu')
        opts.add_argument('--disable-crash-reporter')
        opts.add_argument('--disable-extensions')
        opts.add_argument('--disable-infobars')
        opts.add_argument('--disable-notifications')
        opts.add_argument('--disable-in-process-stack-traces')
        opts.add_argument('--disable-logging')
        opts.add_argument('--disable-dev-shm-usage')
        opts.add_argument('--log-level=3')
        opts.add_argument('--output=/dev/null')
        try:
            self.driver = webdriver.Chrome(
                executable_path=DRIVER_PATH,
                chrome_options=opts
            )
        except Exception as e:
            print(e.with_traceback(None))
            print('Неверный путь к браузеру или к веб драйверу')
            quit(2)
        else:
            try:
                self.driver.get('https://messages.google.com/web/authentication')
            except Exception as e:
                print(e.with_traceback(None))
                print('Не удаётся подключиться к сети интернет')
                quit(2)
        self.find: WebElement = lambda s: WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, s))
        )
        self.find_all: WebElement = lambda s: WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, s))
        )
    
    def __enter__(self):
        """
        Метод нужен для использования оператора with
        """
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Автоматическое закрытие браузера при использовании оператора with
        """
        self.close()
    
    def close(self) -> None:
        """
        Ручное закрытие браузера
        """
        try:
            self.driver.close()
        except Exception as e:
            pass
    
    def sleep(self, sec=0.5) -> 'GoogleBot':
        """
        Вызов таймера между командами, для предотвращения блокировки от сайта
        Можно вызывать 'цепочкой':
        self.sleep().check_connection()
        """
        time.sleep(sec)
        return self
        
    def login(self) -> 'GoogleBot':
        """
        Если уже выполнена авторизация, ничего не происходит
        Иначе, авторизуется на сайте
        """
        for _ in range(6):
            if self.driver.current_url == 'https://messages.google.com/web/conversations':
                self.check_connection()
                return self
            else:
                self.sleep(0.1)
        try:
            remember_toggle = self.find('#mat-mdc-slide-toggle-1-button')
            # поиск qr кода
            self.find('mw-qr-code')
        except Exception as e:
            print(e.with_traceback(None))
            print('Не удалось найти qr код')
            quit(2)
        else:
            print(remember_toggle.get_attribute('class'))
            if 'mdc-switch--unselected' in remember_toggle.get_attribute('class'):
                remember_toggle.click()
            print('Отсканируйте QR код на экране')
            self.sleep().check_connection()
            return self
    
    def check_connection(self) -> None:
        """
        Проверка подключения перед дальнейшей работой
        """
        for _ in range(6):
            try:
                new_msg_button = self.find('mw-fab-link.start-chat a')
            except NoSuchElementException:
                self.sleep()
            else:
                print('Успешно подключено!')
                new_msg_button.click()
                return
        print('Не удалось подключиться к Google!')
        quit(2)
    
    def send_message(self, phone: str, text: str) -> bool:
        """
        Отправка сообщения
        :param phone: номер телефона
        :param text: текст сообщения
        :return: True если сообщение отправилось, False иначе
        """
        self.sleep().__input_phone(phone)
        self.sleep().__confirm_phone()
        status = self.sleep().__send_msg(text)
        return status

    def __input_phone(self, phone: str) -> None:
        """
        Ввод номера телефона
        """
        try:
            input_field = self.find('input.input')
        except Exception as e:
            print(e.with_traceback(None))
            print('Не удалось найти поле для ввода номера телефона')
            quit(2)
        else:
            input_field.send_keys(phone)

    def __confirm_phone(self) -> None:
        """
        Подтверждение номера и переход к вводу текста
        """
        try:
            confirm_phone_btn = self.find('mw-contact-selector-button.ng-star-inserted button')
        except Exception as e:
            print(e.with_traceback(None))
            print('Не удалось подтвердить номер телефона')
            quit(2)
        else:
            confirm_phone_btn.click()
    
    def __send_msg(self, text: str) -> bool:
        """
        Ввод текста и отправка
        :param text: текст сообщения
        :return: True если сообщение отправилось, False иначе
        """
        try:
            input_field = self.find('textarea.input')
            send_text = self.find('mw-message-send-button.ng-star-inserted button')
        except Exception as e:
            print(e.with_traceback(None))
            return False
        else:
            input_field.send_keys(text)

            if '--test' not in sys.argv:
                send_text.click()
            print('Сообщение отправлено!')
            return True

def main(phone, msg):
    """
    Главная функция, используется для запуска скрипта
    """
    import sys
    print(sys.argv)
    for path in (DATA_PATH_GOOGLE, DRIVER_PATH):
        if not os.path.exists(path):
            os.makedirs(path)
        
    with GoogleBot(DATA_PATH_GOOGLE, DRIVER_PATH) as google_bot:
        google_bot.login()
        try:
            pass # phone = phone
        except Exception as e:
            print(e.with_traceback(None))
            print('Не удалось найти номер телефона')
        else:
            print(f'Отправка смс на номер {phone}')
            
#        msg = input('Введите текст сообщения: ')
        status = google_bot.send_message(phone, msg)
        return status


if __name__ == '__main__':
    main()
