#-*- coding: utf-8 -*-
#!/usr/bin/python3

import stmpib, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

id = 'tlsthr33902'
password = '비밀번호를 입력하시면 됩니다.'
sendEmail = 'tlsthr33902@naver.com'
subject = '제목'
text = '내용'
addrs = ['tlsthr33902@naver.com']

smtp = smtplib.SMTP('smtp.naver.com',587)
smtp.ehlo()
smtp.starttls()
smtp.login(id,password)

message = MIMEMultipart()
message.attach(MIMEText(text))

for addr in addrs:
  message['From'] = sendEmail
  message['To'] = addr
  message['Subject'] = subject
  smtp.sendmail(sendEmail,addr,message.as_string())

smtp.quit()
