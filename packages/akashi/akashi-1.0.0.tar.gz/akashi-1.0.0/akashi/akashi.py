import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

punch_element = { "attend": "出勤", "leave": "退勤" }

def akashi(command_type, company, username, password,
            headless=True, mute_audio=False):
    options = Options()
    if headless:
        options.add_argument('--headless')
    if mute_audio:
        options.add_argument('--mute-audio')
    driver = webdriver.Chrome(chrome_options=options)

    driver.get('https://atnd.ak4.jp/login')

    driver.find_element_by_id('form_company_id').send_keys(company)
    driver.find_element_by_id('form_login_id').send_keys(username)
    driver.find_element_by_id('form_password').send_keys(password+Keys.ENTER)

    driver.get('https://atnd.ak4.jp/mypage/punch')

    driver.find_element_by_link_text(punch_element[command_type]).click()

    time.sleep(3)

    driver.quit()