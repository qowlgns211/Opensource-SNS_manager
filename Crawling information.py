#/usr/bin/python3
#-*- coding : utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup

es_host = "127.0.0.1"
es_port = "9200"
Dictionary = {}

def hfilter(s):
  for sentence in s:
    word = sentence.text
    for x in word:
      if(x in word):
        Dictionary[x] += 1
      else:
        Dictionary[x] = 1
        
if __name__ == '__main__':
  url = ' ' # 로그인 후 https 를 받아오는 
  # url 을 받아오는 작업
  
  response = requests.get(url)
  
  if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    ul = soup.select_one('div.content')
    list1 = soup.find_all('title')
    hfilter(list1)
    
    key = list(list1.keys())
    value = list(list1.values())
    
    # Dictionary 형태로 분석 ( 향후 계획 )
  
