import smtplib
import email
from deets import *

def mails(user,starttime,endtime,password,ssid):
    sent_from=gmail_user
    to=emailAddrs
    to.extend([user+emdomain])
    print(to)
    subject="Guest Wifi Scheduled"
    body=user+' scheduled the Guest Wifi from '+starttime+' until '+endtime+'.\nThe network is '+ssid+' and the password is '+password

    email_text="""\
    From: %s
    To: %s
    Subject: %s 

    %s
    """ % (sent_from,", ".join(to),subject,body)

    server=smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user,gmail_password)
    server.sendmail(sent_from,to,email_text)
    server.close()
