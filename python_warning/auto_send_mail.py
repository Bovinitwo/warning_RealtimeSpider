#!usr/bin/env python
#coding=utf-8

import sys
import os
from email.mime.text import MIMEText
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')
#参数1：接受邮箱列表 2：标题 3：正文
def send_mail(mailto_list,sub,content):
	mail_host="smtp.exmail.qq.com"
	mail_user="monitor@mioji.com"
	mail_pass="Mioji@2015Monitor"
	mail_postfix="mioji.com"
	me = "验证监控探针" + "<" + "monitor@mioji.com" + ">"

	msg = MIMEText(content ,_charset='utf-8')
	
	if not isinstance(sub, unicode):
		sub = unicode(sub)
	msg['Subject'] = sub
	msg['From'] = me
	msg['To'] = mailto_list

	try:
		s = smtplib.SMTP()
		s.connect(mail_host)
		s.login(mail_user,mail_pass)
		_items=mailto_list.split(";")
		s.sendmail(me,_items,msg.as_string())
		s.close()
		return True
	except Exception, e:
		print str(e)
		return False


def excute(content,e_address,sub):
    
    if '@' not in e_address:
        to = 'bixin@mioji.com'
    else:
    #to='zhangyang@mioji.com;liuyuan@mioji.com;lurong@mioji.com;dengzhilong@mioji.com'
        to = str(e_address)
    
    d = str(datetime.date.today())
    sub += d
    if send_mail(to, sub, content):
        print 'GOOD!'
    else:
        print 'BAD!'


if __name__=='__main__':
    pass
