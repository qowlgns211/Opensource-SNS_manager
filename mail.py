#-*- coding: utf-8 -*-
#!/usr/bin/python3

import stmpib
from email.message import EmailMessage

email_form = "tlsthr3392@gmail.com"
email_to = "tlsthr3392@gmail.com"
email_subject = "제목을 위한 코드입니다."
email_content = "내용을 위한 코드입니다."

msg = EmailMessage()
msg.set_content(email_content)
msg['From'] = email_from
msg['To'] = email_to
msg['Subject'] = email_subject

smtp = smtplib.SMTP('smtp.gmail.com',587)
smtp = starttls()

smtp.login('tlsthr3392@gmail.com',gmail비밀번호)
smtp.send_message(msg)

smtp.quit()
