#/usr/bin/python3
#-*- coding = utf-8 -*-

import pyperclip
import requests
from flask import Flask render_template
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action\_chains import ActionChains
import time

def copy\_paste(driver, element, text):
  pyperclip.copy(text)
  element.click()
  
  #ActionChains : 명령어들을 모으는 역할이다.
  #ActionChains.perform() : 모인 명령어를 chain 으로 묶인 순서대로 진행한다.
  
  action\_chain = ActionChains(driver).key\_down(Keys.CONTROL).send\_keys('v').key\_up(Keys.CONTROL)
  action\_chain.perform()
  time.sleep(1)
  
if __name__ == '__main__':
  naver_login_url = 'https://nid.naver.com/nidlogin/login'
  id = ' ' # 정보 받아오는 부분 (구현 예정) 
  pwd = '  ' #정보 받아오는 부분  ( 구현 예정)
  
  # flask 로 login 정보 password 정보 받아오기.
  
  driver = Chrome()
  driver.get(naver_login_url)
  id_input = driver.find_element_by_id('id')
  pwd_input = driver.find_element_by_id('pw')
  btn = driver.find_element_by_css_selector('input[type=submit]')
  
  copy\_paste(driver, id\_input, id)
  copy\_paste(driver, pwd\_input,pwd)
