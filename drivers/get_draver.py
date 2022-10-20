from selenium import webdriver


def get(options):
    # прописать какой драйвер использовать при разных ос
    driver = webdriver.Chrome('drivers\chrome_win.exe', chrome_options=options)
    return driver
