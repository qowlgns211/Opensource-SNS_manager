from flask import Flask
from flask import render_template
from flask import request
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup


def Naver(id_input, pwd_input):
    driver = webdriver.Chrome('C:\Chrome_WebDriver\chromedriver.exe')
    #driver.get('https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')
    driver.get('https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')
    # sleep 을 받는 이유는 너무 빠르게 로그인을 해버리면 트래픽공격으로 오해를 받을 수 있다.
    sleep(0.5)
    driver.find_element_by_name("id").send_keys('id_input')
    sleep(0.5) 
    driver.find_element_by_name('pw').send_keys('pwd_input')
    sleep(0.5)
    #아이디와 비밀번호를 자동으로 타이핑하는 코드


    driver.find_element_by_xpath('//*[@id="log.login"]').click()
    #자동으로 로그인 버튼을 눌러주는 코드

def Crawl():
    driver.get("https://mail.naver.com/")
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')

    title_list = soup.find_all('strong','mail.title')
    send_people = soup.find_all('a','title')

    
    for title in title_list:
        print(title.text)
    
    for people in send_people:
        print(people.text)


