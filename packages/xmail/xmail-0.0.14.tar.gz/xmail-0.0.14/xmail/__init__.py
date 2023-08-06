# coding: utf-8
#!/usr/bin/python

"""
@auther: Jiang Long
"""


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

import os

class Xmail(object):
    def __init__(self):
        self.__sender = ""
        self.__passwd = ""
        self.__smtp_server = ""
        self.__attaches = []

    def login(self, sender, passwd):
        self.__sender = sender
        self.__passwd = passwd
        self.__set_smtp(sender)
        return self

    def __set_smtp(self, sender):
        if '@qq.com' in sender:
            self.__smtp_server = 'smtp.qq.com'
        else:
            self.__smtp_server = 'smtp.exmail.qq.com'

    def send_mail(self, to, mail):
        try:
            message = MIMEMultipart()
            message['From'] = formataddr([self.__sender, self.__sender])
            message['To'] = formataddr([to, to])
            message['Subject'] = mail['subject']
            message.attach(MIMEText(mail['content'], 'plain', 'utf-8'))
            for attach in self.__attaches:
                message.attach(attach)
            server = self.__init_server()
            server.sendmail(self.__sender, [to,], message.as_string())
            server.quit()
        except Exception as e:
            print(e)

    def __init_server(self):
        server = smtplib.SMTP_SSL(self.__smtp_server, 465)
        server.login(self.__sender, self.__passwd)
        return server

    def add_attach(self, path):
        attach = MIMEText(open(path, 'rb').read(), 'base64', 'utf-8')
        attach['Content-Type'] = 'application/octet-stream'
        attach['Content-Disposition'] = 'attachment; filename={}'.format(os.path.basename(path))
        self.__attaches.append(attach)
        return self

