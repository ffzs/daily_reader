import requests
import json
import re
import random
import time
import datetime
import os
import pdfkit
from USA import *

def make_dir(name):
    isExists = os.path.exists(name)
    if not isExists:
        os.makedirs(name)
        return True
    else:
        return False

def get_yesterday():
    return datetime.date.today() - datetime.timedelta(days=1)

def get_day(timeStamp):
    return datetime.date.fromtimestamp(timeStamp)

if __name__ == '__main__':
    names, numbers = [], []
    for line in open('gongzhonghao.txt', 'r', encoding='utf-8'):
        names.append(line.split('|')[0])
        numbers.append(line.split('|')[1])
    yesterday = get_yesterday()
    make_dir(str(yesterday))
    url = 'https://mp.weixin.qq.com'
    header = {
        "HOST": "mp.weixin.qq.com",
        "User-Agent": random.choice(USA_TRY)
        }
    with open('cookie.txt', 'r', encoding='utf-8') as f:
        cookie = f.read()
    cookies = json.loads(cookie)
    response = requests.get(url=url, cookies=cookies)
    token = re.findall(r'token=(\d+)', str(response.url))[0]
    for i, query in enumerate(numbers):
        query_id = {
            'action': 'search_biz',
            'token' : token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'query': query,
            'begin': '0',
            'count': '5',
        }
        search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
        search_response = requests.get(search_url, cookies=cookies, headers=header, params=query_id)
        lists = search_response.json().get('list')[0]
        fakeid = lists.get('fakeid')
        query_id_data = {
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'action': 'list_ex',
            'begin': '0',
            'count': '5',
            'query': '',
            'fakeid': fakeid,
            'type': '9'
        }
        appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
        appmsg_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
        max_num = appmsg_response.json().get('app_msg_cnt')
        num = int(int(max_num) / 5)
        begin = 0
        file_num = 0
        the_day = ""
        while num + 1 > 0 :
            query_id_data = {
                'token': token,
                'lang': 'zh_CN',
                'f': 'json',
                'ajax': '1',
                'random': random.random(),
                'action': 'list_ex',
                'begin': '{}'.format(str(begin)),
                'count': '5',
                'query': '',
                'fakeid': fakeid,
                'type': '9'
            }
            print('翻页###################', begin, names[i])
            query_fakeid_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
            fakeid_list = query_fakeid_response.json().get('app_msg_list')
            for item in fakeid_list:
                timeStamp = int(item.get('update_time'))
                day = get_day(timeStamp)
                if day != the_day:
                    the_day = day
                if day == yesterday:
                    file_name = '{}@{}({}).pdf'.format(names[i], yesterday, file_num)
                    file_num += 1
                    pdfkit.from_url(item.get('link'), '{}/{}'.format(yesterday, file_name))
                    with open(str(yesterday) + '/info.txt', 'a', encoding='utf-8') as f:
                        print(item.get('title').strip())
                        print(item.get('link'))
                        f.write('{}${}${}${}\n'.format(names[i], item.get('title').strip(), item.get('link'), file_name))
            num -= 1
            begin = int(begin)
            begin += 5
            print('################等待###############')
            time.sleep(random.choice([10, 15, 20]))
            if the_day < yesterday:
                break