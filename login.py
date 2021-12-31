import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import getpass
'''import logging
logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(message)s',
    datefmt='%Y%m/%d %I:%M:%S %p',
    level=logging.DEBUG
)'''
import time
import datetime

def run(id, pw):
    # "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    options = webdriver.ChromeOptions();
    options.add_experimental_option("detach", True)
    options.add_argument('--disable-logging')
    driver = webdriver.Chrome("./chromedriver.exe", options=options)

    driver.get('https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')

    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'log.login'))
        )
    except:
        print('{:s}|login|로그인 화면 로딩 실패'.format(str(datetime.datetime.now())))
        return None;

    driver.execute_script("document.getElementById('id').value = \'" + id + "\'")
    driver.execute_script("document.getElementById('pw').value = \'" + pw + "\'")
    #driver.find_element(By.ID, 'id').send_keys(id)
    #driver.find_element(By.ID, 'pw').send_keys(pw)
    driver.find_element(By.ID, 'log.login').click()

    time.sleep(1)

    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'err_common'))
        )
        #elmerrmsg = driver.find_element(By.ID, '#err_common > div')
        elmerrmsg = driver.find_element(By.ID, 'err_common')
        errmsg = elmerrmsg.text
        print('{:s}|login|로그인 실패'.format(str(datetime.datetime.now())))
        return None;
    except:
        print('{:s}|login|아이디, 패스워드 성공'.format(str(datetime.datetime.now())))

    try:
        print('{:s}|login|2단계 인증 중'.format(str(datetime.datetime.now())))
        WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'input_text'))
        )
    except:
        print('{:s}|login|2단계 인증 시간 5분 초과'.format(str(datetime.datetime.now())))
        return None

    print('{:s}|login|로그인 성공'.format(str(datetime.datetime.now())))

    return driver


if __name__ == '__main__':
    userid = input("enter your id:")
    pw = getpass.getpass("enter your password:")

    run(userid, pw)

    exit()