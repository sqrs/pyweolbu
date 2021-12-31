import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import getpass
'''import logging
logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(message)s',
    datefmt='%Y%m/%d %I:%M:%S %p',
    level=logging.DEBUG
)'''
import login
import checknotice
import leavecomment
import time
import datetime


def main():
    isreal = False
    version = 'test'
    if len(sys.argv) > 1:
        isreal = True
        version = 'real'

    print('{:s} version'.format(version))
    print('ChromeDriver 96.0.4664.18')
    print('강제 종료 : Ctrl+C')
    userid = input("enter your id:")
    pw = getpass.getpass("enter your password:")

    # LOGIN
    driver = login.run(userid, pw)

    if driver is None:
        print('에러 종료(driver is None)')
        return -1;
    else:
        print('{:s}|main|next : 공지 체크'.format(str(datetime.datetime.now())))

    # GO TO NOTICE COMMENT
    resultchecknotice = checknotice.run(driver, '본공지', isreal)
    resultleavecomment = False

    if resultchecknotice:
        # LEAVE A COMMENT
        print('{:s}|main|next : 댓글 작성'.format(str(datetime.datetime.now())))
        resultleavecomment = leavecomment.run(driver)
    else:
        print('{:s}|main|error : 공지 체크'.format(str(datetime.datetime.now())))
        print('에러 종료(checknotice fail)')
        return -1;

    print('{:s}|main|정상 종료'.format(str(datetime.datetime.now())))
    return 0


if __name__ == '__main__':
    main()