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
    driver.get('https://logins.daum.net/accounts/signinform.do?url=https%3A%2F%2Fwww.daum.net%2F')
    sleep(0.5)
    driver.find_element_by_name('id').send_keys('id_input')
    sleep(0.5)
    driver.find_element_by_name('pw').send_keys('pwd_input')
    sleep(0.5)

    driver.find_element_by_xpath('//*[@id="loginBtn"]').click()
    sleep(0.5)

    #메일 안의 내용 받아오기

    driver.get("https://mail.daum.net/")
    sleep(0.5)

    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')

    mailList = driver.find_elements_by_css_selector('a.link_from')

    for link in mailList:
        #dic['person'] = link.get('title')
        #print(dic['person'])
        #dic['title'] = link.text.strip()
        #print(dic['title'])
        #dic['address'] = link.get('href')
        #print(dic['address'])

        print(link.text)
    
def Naver(id_input, pwd_input):
    dic = {'person' : "Root" , 'title' : "관리자",'address' : "주소" }

    driver = webdriver.Chrome('C:\Chrome_WebDriver\chromedriver.exe')
    sleep(0.5)
    driver.get('https://mail.naver.com')
    driver.find_element_by_name('id').click()
    pyperclip.copy('id_input')
    driver.find_element_by_name('id').send_keys(Keys.CONTROL,'v')
    sleep(0.5)
    driver.find_element_by_name('pw').click()
    pyperclip.copy('pwd_input')
    driver.find_element_by_name('pw').send_keys(Keys.CONTROL,'v')
    sleep(0.5)
    driver.find_element_by_id('log.login').click()

    maillist = driver.find_elements_by_css_selector('strong.mail_title')
    for mail in maillist:
        print(mail.text)
        


