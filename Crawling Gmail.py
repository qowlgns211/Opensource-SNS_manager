#/usr/bin/python3
#-*- coding = utf-8 -*-

from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time

driver = webdriver.Chrome()
url = 'https://www.google.com'
driver.get(url)

# 엑션체인으로 driver 조작
action = ActionChains(driver)

# 로그인 버튼의 id값(gb_70) 클릭 // id는 #, class는 . 으로 구분
driver.find_element_by_css_selector('#gb_70').click()

# 커서가 바로 로그인 하는 곳을 가르키기 때문에 바로 엑션을 취함
# - send_keys로 데이터를 보내고 perform으로 동작
# - reset_action은 밑에 있는 다른 action을 위해 초기화 해줌
# - 다음 버튼(.Cwak9)을 클릭
# - 로그인 동안 대기시간 2초
action.send_keys('id').perform()
time.sleep(2)
action.reset_actions()
time.sleep(2)
# action.reset_actions()
driver.find_element_by_css_selector('.CwaK9').click()
time.sleep(5)

# 비밀번호를 입력
# - 커서를 위치하기 위해 비밀번호 창의 클레스 값에 비밀번호 입력
# - 다음 버튼 누르고
# - 로그인을 위해 2초 대기
driver.find_element_by_css_selector('.whsOnd.zHQkBf').send_keys('passward')
driver.find_element_by_css_selector('.CwaK9').click()
time.sleep(5)

# 이메일 보내기 위해 메일 링크로 들어감
driver.get('https://mail.google.com/mail/u/0/?ogbl#inbox')
time.sleep(5)

# 이메일 쓰기 버튼의 클레스를 찾아서 클릭
driver.find_element_by_css_selector('.T-I.J-J5-Ji.T-I-KE.L3').click()
time.sleep(5)

send_button = driver.find_element_by_css_selector('.T-I.J-J5-Ji.aoO.v7.T-I-atl.L3')
mail_button = driver.find_element_by_css_selector('.wO.nr')

# () 으로 묶어주면 1줄처럼 파악함
(
action.send_keys('@gmail.com') #오류 부분
.key_down(Keys.TAB).pause(1).key_down(Keys.TAB).pause(2) # 받는 사람을 적고 TAB 2번 누르기
.send_keys('제목입니다.').pause(2).key_down(Keys.TAB).pause(2) # 제목 입력 부분 탭으로 다음칸
.send_keys('abcde').pause(2).key_down(Keys.ENTER) # 내용 입력 부분
.key_down(Keys.SHIFT).send_keys('abcd').key_up(Keys.SHIFT).pause(2) # Key_down은 up을 해주기 전까지 눌러줌
.move_to_element(send_button).click()
.perform() # 실행
)