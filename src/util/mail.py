# -*- coding: utf-8 -*-

from email.header import Header
from email.mime.text import MIMEText
import smtplib

from_addr = 'je_shrine@163.com'
password = 'shrine,123'
to_addr = '505968815@qq.com'
smtp_server = 'smtp.163.com'

def sendTo(to, subject, body):

    try:
        msg = MIMEText(body, 'plain', 'utf-8')

        msg['From'] = '自由神社 <%s>' % (from_addr)
        msg['To'] = '<%s>' % (to_addr)
        msg['Subject'] = Header(subject, 'utf-8')

        server = smtplib.SMTP(smtp_server, 25)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to], msg.as_string())
        server.quit()

    except Exception as error:
        print('邮件发射失败', error)
        return False

    return True

if __name__ == '__main__':
    # sendTo(to_addr, '验证电子邮件地址', '你好')
    sendTo(to_addr, '验证电子邮件地址', '感谢您注册自由神社账户\n\n点击此链接验证您的电子邮件\n\nhttp://localhost:5000\n')
