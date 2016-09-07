# -*- coding: utf-8 -*-

import sys
sys.path.append('/search/python_warning')
import os
import time
import datetime
import re
import json
import redis
import auto_send_mail
#from send_mail import send_mail

EMAIL_ADDRESS = 'liuyu@mioji.com;chaisiyuan@mioji.com;dengzhilong@mioji.com;yuyang@mioji.com'
TITLE='验证服务堆积报警'

queue_pat = re.compile(r'size of queue: (.*?)$')
OVER_QUEUE=50

redis_ob = redis.Redis(host = 'localhost',port = 6379 ,db = 9)

log_dir1 = "/search/RealtimeSpider/"
log_dir2 = "/search/realtime_log_2/"
def get_filename(log_dir):
    '''
    get the logs
    '''
    all_file = os.listdir(log_dir)
    for index in range(0,len(all_file)):
        all_file[index]=log_dir+all_file[index]
    file_name = ''
    for each_file in all_file:
        if re.match(r'.*20.*_\d\d\.log$',each_file) and os.path.isfile(each_file):
            time = datetime.datetime.strptime(each_file[-15:-4],'%Y%m%d_%H')
            if time>=datetime.datetime.now()-datetime.timedelta(hours=1):
                file_name = str(each_file)
    return file_name
def is_overload(file_name,redis_key):
    '''
    确认是否(size of queue >= 50的次数)大于或等于10次
    是则返回True
    否则返回False
    '''
    over_times=0
    shell_code = 'grep "size of queue" %s > /search/python_warning/tmp_log' % file_name
    os.system(shell_code)
    with open('/search/python_warning/tmp_log') as f:
        for line in f:
            content = queue_pat.search(line).groups()
            queue_length = content[0]
            if int(queue_length) >= 50:
                over_times += 1
    currentTotal = over_times - int(read_preTotal(redis_key))
    save_preTotal(over_times,redis_key)

    time = str(datetime.datetime.now())
    time = time[0:time.find('.')]
    content = str(file_name)+'\n'+str(time) + str('\n前十分钟队列长度超出50的次数为:')+str(currentTotal)

    print 'content',content
    if int(currentTotal)>=10:
        return True,content
    else:
        return False,content
def read_preTotal(redis_key):
    '''
    读取之前的preTotal
    '''
    preTotal = redis_ob.get(redis_key) 
    return preTotal

def save_preTotal(preTotal,redis_key):
    '''
    保存之前的size of queue超过50的总次数
    '''
    time = int(str(datetime.datetime.now())[14:16])
    if time>=59 or time<9:
        redis_ob.set(redis_key,0)    
    else:
        redis_ob.set(redis_key,preTotal)

if __name__ == '__main__':
    file_name1 = get_filename(log_dir1)
    warning1,content1 = is_overload(file_name1,'RealtimeSpider')
    file_name2 = get_filename(log_dir2)
    warning2,content2 = is_overload(file_name2,'realtime_log_2')

    content = content1+'\n\n'+content2
    if warning1 or warning2 :
        auto_send_mail.excute(content,EMAIL_ADDRESS,TITLE)




