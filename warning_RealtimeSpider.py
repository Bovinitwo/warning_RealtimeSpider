# -*- coding: utf-8 -*-

import sys
sys.path.append('/search/uid_CN')
import os
import time
import datetime
#import db_local as db
from DBHandle import DBHandle
import re
import json
import redis
#from send_mail import send_mail

queue_pat = re.compile(r'size of queue:(.*?)')
OVER_QUEUE=50

redis_ob = redis.Redis(host = 'localhost',port = 6379 ,db = 9)

log_dir1 = "/search/RealtimeSpider/"
log_dir2 = "/search/realtime_log/"
log_dir3 = "/search/realtime_log_2/"
def get_filename():
    '''
    get the logs
    '''
    all_file1 = os.listdir(log_dir1)
    all_file2 = os.listdir(log_dir2)
    all_file3 = os.listdir(log_dir3)
    for index in range(0,len(all_file1)):
        all_file1[index]=log_dir1+all_file1[index]
    for index in range(0,len(all_file2)):
        all_file2[index]=log_dir2+all_file2[index]
    for index in range(0,len(all_file3)):
        all_file3[index]=log_dir3+all_file3[index]

    all_files = all_file1+all_file2+all_file3
    files=[]
    if sys.argv[1]=="-hour":
        for each_file in all_files:
            if re.match(r'.*20.*_\d\d\.log$',each_file) and os.path.isfile(each_file):
                time = datetime.datetime.strptime(each_file[-15:-4],'%Y%m%d_%H')
                if time<=datetime.datetime.now()-datetime.timedelta(hours=1):
                    files.append(each_file)
    return files
def is_overload(files):
    '''
    确认是否(size of queue >= 50的次数)大于或等于10次
    是则返回True
    否则返回False
    '''
    over_times=0
    files = sorted(files)
    for file_name in files:
        shell_code = 'grep "size of queue" %s > /home/liuyu/python_warning/tmp_log' % file_name
        os.system(shell_code)
        with open('/home/liuyu/python_warning/tmp_log') as f:
            for line in f:
                content = queue_pat.search(line).groups()
                queue_length = content
                if queue_length >= 50:
                    over_times += 1
    save_preTotal(over_times)
    currentTotal = over_times - read_preTotal()
    if currentTotal>=10:
        is_warning = True
    else:
        is_warning = False
    return is_warning

def read_preTotal()
    '''
    读取之前的preTotal
    '''
    preTotal = redis_ob.get('preTotal') 
    return preTotal

def save_preTotal(preTotal)
    '''
    保存之前的size of queue超过50的总次数
    '''
    time = int(str(datetime.datetime.now())[14:16])
    if time>=59 or time<9:
        redis_ob.set('preTotal',0)    
    else:
        redis_ob.set('preTotal',preTotal)
def senf_mail():
    '''
    发送邮件
    '''

if __name__ == '__main__':
    '''
    files = get_filename()
    '''
    files = []
    files.append('/home/liuyu/python_warning/')
    warning = is_overload(files)
    if is_warning :
        send_email()
