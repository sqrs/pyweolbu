import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import getpass
import login
import checknotice
import time
import datetime

def run(driver):
    while True:
        # div.nodata : no comment, ul.comment_list : comment exists
        # wait for comments loaded
        try:
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'TownCommentComponent'))
            )
        except:
            driver.refresh()
            continue

        # nodata class? there is no comment yet. refresh
        try:
            driver.find_element(By.CLASS_NAME, 'nodata')
            print('{:s}|leavecomment|댓글 없음. 새로고침'.format(str(datetime.datetime.now())))
            driver.refresh()
            continue
        except:
            print('{:s}|leavecomment|댓글 있음'.format(str(datetime.datetime.now())))

        # if there are comments, there must be comment_list class
        try:
            driver.find_element(By.CLASS_NAME, 'comment_list')
            print('{:s}|leavecomment|댓글(comment_list) 확인'.format(str(datetime.datetime.now())))
        except:
            print('{:s}|leavecomment|댓글 목록 없음. 새로고침'.format(str(datetime.datetime.now())))
            driver.refresh()
            continue;

        #  list라서 예외없지만 만약을 대비해서 try
        elements = None
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, 'ul.comment_list > li')
            print('{:s}|leavecomment|댓글(comment_list > li) 확인'.format(str(datetime.datetime.now())))
        except:
            print('{:s}|leavecomment|댓글 리스트 없음. 새로고침'.format(str(datetime.datetime.now())))
            driver.refresh()
            continue

        if len(elements) < 10:
            print('{:s}|leavecomment|댓글 수 부족. 새로고침'.format(str(datetime.datetime.now())))
            driver.refresh()
            continue

        succ_comment = False

        while True:
            try:
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#app > div > div > div.comment_textarea_wrap > div'))
                )

                # click comment area
                driver.find_element(By.CSS_SELECTOR, '#app > div > div > div.comment_textarea_wrap > div').click()
                # write a comment
                driver.find_element(By.CLASS_NAME, 'text_input_area').send_keys('q')
            except:
                print('{:s}|leavecomment|댓글창 비활성화 1초 이상 걸림. 새로고침'.format(str(datetime.datetime.now())))
                driver.refresh()
                continue

            # click to register a comment when the button is clickable
            try:
                WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, 'btn_done')))
                driver.find_element(By.CLASS_NAME, 'btn_done').click()
            except:
                print('{:s}|leavecomment|버튼 비활성화 1초 이상 걸림. 새로고침'.format(str(datetime.datetime.now())))
                driver.refresh()
                continue

            try:
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.dismiss()
                #alert.accpet() # accept()시 except 발생
                driver.refresh()
                continue
            except:
                succ_comment = True
                break

        if succ_comment:
            break

    return True


if __name__ == '__main__':
    userid = input("enter your id:")
    pw = getpass.getpass("enter your password:")

    isreal = False
    if len(sys.argv) > 1:
        isreal = True

    driver = login.run(userid, pw)

    resultchecknotice = False
    if driver:
        resultchecknotice = checknotice.run(driver, '본공지', isreal)
    else:
        print('{:s}|leavecomment(test)|error : 로그인에서 에러'.format(str(datetime.datetime.now())))
        exit()

    if not resultchecknotice:
        print('{:s}|leavecomment(test)|error : 공지 체크에서 에러'.format(str(datetime.datetime.now())))
        exit()

    resultleavecomment = run(driver)
    if not resultleavecomment:
        print('{:s}|leavecomment(test)|error : 댓글 작성에서 에러'.format(str(datetime.datetime.now())))
        exit()

    exit()
