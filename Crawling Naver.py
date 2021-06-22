import pyperclip

from flask import Flask
from flask import render_template
from flask import request
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

def Daum(id_input,pwd_input):

    #각각의 정보 리스트
    D_person = []
    D_title = []
    D_address = []

    # 로그인 하는 과정

    driver = webdriver.Chrome('C:\Chrome_WebDriver\chromedriver.exe')
    driver.get('https://mail.daum.net/')
    driver.find_element_by_xpath('//*[@id="daumHead"]/div/div/a[4]/span').click()
    driver.find_element_by_xpath('//*[@id="mArticle"]/div[1]/div/div/div[2]/a[2]').click()
    driver.find_element_by_name('id').send_keys('spross9970')
    sleep(0.5)
    driver.find_element_by_name('pw').send_keys('pass9970')
    sleep(0.5)
    driver.find_element_by_xpath('//*[@id="loginBtn"]').click()
    sleep(0.5)

    #메일 안의 내용 받아오기

    driver.get('https://mail.daum.net/')
    print(driver.page_source)

    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')

    mails = soup.select('#mailList > div.scroll > div > ul > li')

    for mail in mails:
        Person = mail.select_one('div.info_from > a')['title']
        Title = mail.select_one('div > a > strong').text
        Address = mail.select_one('div.info_subject > a')['href']
        D_person.append(Person)
        D_title.append(Title)
        D_address.append('https://mail.daum.net/' + Address)

    # 드라이버 종료
    driver.quit()

    
def Naver(id_input, pwd_input):
    #전체 리스트 변수
    N_person= []
    N_address = []
    N_title = []


    #옵션 생성
    #options = webdriver.ChromeOptions()

    #창 숨기는 옵션 추가
    #options.add_argument("headless")
    #options.add_argument('window-size=1920x1080')
    #options.add_argument('disable-gpu')
    #options.add_argument("lang=ko_KR")

    #드라이버 실행시키기
    driver = webdriver.Chrome('C:\Chrome_WebDriver\chromedriver.exe',options = options)
    sleep(0.5)

    driver.get('https://mail.naver.com')
    id_input = 'dkstjsdn1224'
    pwd_input = 'fellin1919'

    # 아이디 패스워드 자동 입력화 부분
    driver.find_element_by_name('id').click()
    pyperclip.copy(id_input)
    driver.find_element_by_name('id').send_keys(Keys.CONTROL,'v')
    sleep(0.5)
    driver.find_element_by_name('pw').click()
    pyperclip.copy(pwd_input)
    driver.find_element_by_name('pw').send_keys(Keys.CONTROL,'v')
    sleep(0.5)

    #로그인 버튼 클릭 자동화
    driver.find_element_by_id('log.login').click()

    #Web 브라우저 받아오기.
    driver.get("https://mail.naver.com/")
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')

    # 보낸 사람 person, 내용 주솟값 각각의 리스트에 포함.
    mails = soup.select('#list_for_view > ol > li')

    for mail in mails:
        Person = mail.select_one('div > div > a')['title']
        Address = mail.select_one('div > div.subject > a')['href']
        N_person.append(Person)
        N_address.append("https://mail.naver.com/" + Address)

    # 메일 제목 title 딕셔너리에 포함.
    maillist = soup.find_all('strong','mail_title')

    for b in maillist:
        N_title.append(b.text)

    # 드라이버 종료
    driver.quit()

