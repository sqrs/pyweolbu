import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import getpass
import login
import time
import datetime
import re

def run(driver, keyword, isreal):
    if isreal:
        driver.get('https://m.cafe.naver.com/ca-fe/wecando7?tab=notice')
    else:
        driver.get('https://m.cafe.naver.com/ca-fe/wecando7?tab=notice')

    found = False
    refreshCnt = 0;
    regext = re.compile("\d+:\d+")
    while refreshCnt < 300:
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#ct > div.list_board > div > ul > li:nth-child(1) > div > a.txt_area > strong'))
            )
            element_first_title = driver.find_element(By.CSS_SELECTOR,
                                                      '#ct > div.list_board > div > ul > li:nth-child(1) > div > a.txt_area > strong')
            title = element_first_title.text
        except:
            refreshCnt = refreshCnt + 1
            driver.refresh()
            continue

        if keyword in title:
            print('{:s}|notice|최신글이 본공지 맞음'.format(str(datetime.datetime.now())))
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,
                                                    '#ct > div.list_board > div > ul > li:nth-child(1) > div > a:nth-of-type(1) > div > span.time'))
                )
                element_notice_time = driver.find_element(By.CSS_SELECTOR,
                                    '#ct > div.list_board > div > ul > li:nth-child(1) > div > a:nth-of-type(1) > div > span.time')
                noticetime = element_notice_time.text
                ret_regext = regext.match(noticetime)
                if not ret_regext:
                    print('{:s}|notice|시간 값이 날짜임(예전 공지)({:s})'.format(str(datetime.datetime.now()), noticetime))
                    refreshCnt = refreshCnt + 1
                    driver.refresh()
                    continue
                else:
                    print('{:s}|notice|시간 값 확인.({:s})'.format(str(datetime.datetime.now()), noticetime))
                    found = True
            except:
                refreshCnt = refreshCnt + 1
                driver.refresh()
                continue

            try:
                print('{:s}|notice|댓글 버튼 클릭'.format(str(datetime.datetime.now())))
                driver.find_element(By.CSS_SELECTOR,
                                    '#ct > div.list_board > div > ul > li:nth-child(1) > div > a.link_comment').click()
                break
            except:
                refreshCnt = refreshCnt + 1
                driver.refresh()
                continue
        else:
            refreshCnt = refreshCnt + 1
            print('{:s}|notice|최신글이 본공지 아님({:s})'.format(str(datetime.datetime.now()), title))
            driver.refresh()
            continue

    if found:
        return True
    else:
        print('{:s}|notice|새로고침 300회 초과'.format(str(datetime.datetime.now())))
        return False

if __name__ == '__main__':
    userid = input("enter your id:")
    pw = getpass.getpass("enter your password:")

    isreal = False
    if len(sys.argv) > 1:
        isreal = True

    driver = login.run(userid, pw)

    if driver:
        run(driver, '본공지', isreal)
    else:
        print('{:s}|checknotice(test)|error : 로그인에서 에러'.format(str(datetime.datetime.now())))

    exit()
