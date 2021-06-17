#-*- coding: utf-8 -*-
#!/usr/bin/python3

import stmpib, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys

def navermail(id,password,sendEmail,subject,text,addrss):
  addrs = [addrss]
  smtp = smtplib.SMTP('smtp.gmail.com',587)
  smtp.ehlo()
  smtp.starttls()
  smtp.login(id,password)

  message = MIMEMultipart()
  message.attach(MIMEText(text))

  for addr in addrs:
    message['From'] = sendEmail
    message['TO'] = addr
    message['Subject'] = subject
    smtp.sendmail(sendEmail,addr,message.as_string())

  smtp.quit()
