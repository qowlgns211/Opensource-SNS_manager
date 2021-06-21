import pyperclip

from flask import Flask
from flask import render_template
from flask import request
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

def Daum(id_inpuut,pwd_input):
    # Dictionary 변수
    # person : 보낸 사람 title : 제목 address : 메일 내용 주소

    dic = {'person' : "ROOT" , 'title' : "관리자", 'address' : "root" }

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

    driver.get("https://mail.daum.net/")

    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')

    maillist = soup.select('#mailList > div.scroll > div > ul > li')
    print(maillist)

    for mail in maillist:
        person = mail.select_one('div> input')['title']
        address = mail.select_one('div > a')['href']
        title = mail.select_one('div > a >strong')
        dic['title'] += title.text
        dic['person'] += person.text
        dic['address']+= address.text
        print(person.text)
        print(address.text)
        print(title.text)
        
def Naver(id_input, pwd_input):
    dic = {'person' : "Root" , 'title' : "관리자",'address' : "root" }

    #드라이버 실행시키기
    driver = webdriver.Chrome('C:\Chrome_WebDriver\chromedriver.exe')
    sleep(0.5)
    driver.get('https://mail.naver.com')

    # 아이디 패스워드 자동 입력화 부분
    driver.find_element_by_name('id').click()
    pyperclip.copy('dkstjsdn1224')
    driver.find_element_by_name('id').send_keys(Keys.CONTROL,'v')
    sleep(0.5)
    driver.find_element_by_name('pw').click()
    pyperclip.copy('fellin1919')
    driver.find_element_by_name('pw').send_keys(Keys.CONTROL,'v')
    sleep(0.5)

    #로그인 버튼 클릭 자동화
    driver.find_element_by_id('log.login').click()

    #Web 브라우저 받아오기.
    driver.get("https://mail.naver.com/")

    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    
    # 보낸 사람 person, 내용 주솟값 address 딕셔너리에 포함.
    mails = soup.select('#list_for_view > ol > li')
    
    for mail in mails:
        person = mail.select_one('div > div > a')['title']
        address = mail.select_one('div > div.subject > a')['href']
        dic['person'] += person.text
        dic['address']+= "https://mail.naver.com/" + address.text

    # 메일 제목 title 딕셔너리에 포함.
    maillist = soup.find_all('strong','mail_title')

    for b in maillist:
        dic['title']+= b.text
        
