#!/usr/bin/python
# -*- coding: utf-8 -*-

import smtplib

from email.mime.text import MIMEText
from smtplib import SMTP_SSL


import sys


def send_mail(to_list, subject, content):
    # mail_to_list = ['fangzhongpeng@iqingka.com','fangzhongpeng9@163.com']
    # mail_to_list = ['fangzhongpeng9@163.com>']
    #mail_host = 'smtp.163.com'
    #mail_user = 'fangzhongpeng9@163.com'
    #mail_pass = 'SUPSQAEZRFQDYVKI'
    #mail_postfix = '163.com'
    mail_host = 'smtp.mxhichina.com'
    mail_user = 'fangzhongpeng@iqingka.com'
    mail_pass = 'Hello1234'
    mail_postfix = 'mxhichina.com'

    # me = mail_user+"<"+mail_user+"@"+mail_postfix+">"
    # msg = MIMEText(content)
    msg = MIMEText(content, _subtype='html',_charset='utf-8')

    msg['Subject'] = subject

    msg['From'] = mail_user

    msg['to'] = ";".join(to_list)

    # msg['to'] = to_list

    try:

        # s = smtplib.SMTP()
        s = SMTP_SSL()

        s.connect(mail_host)

        s.login(mail_user, mail_pass)

        s.sendmail(mail_user, to_list, msg.as_string())

        s.close()

        return True

    except Exception, e:

        print str(e)

        return False


if __name__ == "__main__":
    print sys.argv[1]

    print sys.argv[2]

    print sys.argv[3]

    # send_mail(sys.argv[1], sys.argv[2])
    send_mail(sys.argv[1], sys.argv[2], sys.argv[3])

