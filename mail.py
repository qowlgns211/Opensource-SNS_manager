# -*- coding: utf-8 -*-
#!/usr/bin/python3

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage


def navermail(id, password, sendEmail, subject, text, addrss):

    addrs = [addrss]
    smtp = smtplib.SMTP('smtp.naver.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(id, password)

    message = MIMEMultipart()
    message.attach(MIMEText(text))

    for addr in addrs:
        message['From'] = sendEmail
        message['TO'] = addr
        message['Subject'] = subject
        smtp.sendmail(sendEmail, addr, message.as_string())

    smtp.quit()


def googlemail(email_from, email_to, email_subject, email_content, email_password):

    msg = EmailMessage()
    msg.set_content(email_content)

    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = email_subject

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(email_from, email_password)
    smtp.send_message(msg)

    smtp.quit()
