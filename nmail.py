# -*- coding: utf-8 -*-
#!/usr/bin/python3

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def nmail(id, password, sendEmail, subject, text, addrs):
    smtp = smtplib.SMTP('smtp.naver.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(id, password)

    message = MIMEMultipart()
    message.attach(MIMEText(text))

    message['From'] = sendEmail
    message['To'] = addrs
    message['Subject'] = subject
    smtp.sendmail(sendEmail, addrs, message.as_string())

    smtp.quit()
