#-*- coding: utf-8 -*-

from smtplib import SMTP_SSL


def mail(a,b,c,d,e):

    Eto = a
    Efrom = b
    Etitle = c
    Ebody = d

    Ebody = str(Ebody)
    
    password = e

    msg = "\r\n".join(["From: " + Efrom, "To: " + Eto, "Subject: " + Etitle, "",Ebody])
    conn = SMTP_SSL('smtp.daum.net:465')
    conn.ehlo()
    conn.login(Eto,password)
    conn.sendmail(Efrom,Eto,msg)
    conn.close()
