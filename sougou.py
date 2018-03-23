import pdfkit
import requests
from bs4 import BeautifulSoup as bs
import re
import time
import datetime
from USA import *
import random
import os

def make_dir(name):
    isExists = os.path.exists(name)
    if not isExists:
        os.makedirs(name)
        return True
    else:
        return False

def get_day(datetime):
    return time.strftime("%Y-%m-%d", time.localtime(int(datetime)))

def get_yesterday():
    return str(datetime.date.today() - datetime.timedelta(days=1))

def get_headers():
    headers = {
        'Referer': 'http://weixin.sogou.com/weixin?type=1&s_from=input&query=almosthuman2014&ie=utf8&_sug_=n&_sug_type_=',
        'User-Agent': random.choice(USA_TRY)
    }
    return headers

if __name__ == '__main__':
    yesterday = get_yesterday()
    make_dir(yesterday)
    for line in open('gongzhonghao.txt', 'r', encoding='utf-8'):
        i = 0
        name = line.split('|')[0]
        number = line.split('|')[1]
        print(name, number)
        url = 'http://weixin.sogou.com/weixin?type=1&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_='.format(number)
        headers = get_headers()
        response = requests.get(url, headers=headers)
        soup = bs(response.text, 'lxml')
        href = soup.find('p', class_='tit').find('a')['href']
        headers = get_headers()
        resp = requests.get(href, headers=headers)
        pattern = re.compile(
                'var msgList = (.*?)seajs',
                re.S)
        all_info = eval(re.findall(pattern, resp.text)[0].strip()[:-1])
        for item in all_info["list"]:
            article_url = 'https://mp.weixin.qq.com' + item['app_msg_ext_info']['content_url'].replace(';', '&')
            datetime = item['comm_msg_info']['datetime']
            day = get_day(datetime)
            if day == yesterday:
                article_title = item['app_msg_ext_info']['title']
                file_name = '{}/{}@{}({}).pdf'.format(yesterday, name, day, i)
                pdfkit.from_url(article_url, file_name)
                next_list = item['app_msg_ext_info']['multi_app_msg_item_list']
                with open(yesterday +'/info.txt', 'a+', encoding='utf-8') as f:
                    f.write('{}${}${}${}${}\n'.format(name, article_title, article_url, day, file_name))
                if next_list:
                    for item in next_list:
                        i += 1
                        article_url = 'https://mp.weixin.qq.com' + item['content_url'].replace(';', '&')
                        file_name = '{}/{}@{}({}).pdf'.format(yesterday, name, day, i)
                        article_title = item['title']
                        try:
                            pdfkit.from_url(article_url, file_name)
                        except Exception as e:
                            print(e)
                        with open(yesterday + '/info.txt', 'a+', encoding='utf-8') as f:
                            f.write('{}${}${}${}${}\n'.format(name, article_title, article_url, day, file_name))
                i += 1
        time.sleep(random.choice([2, 3, 4, 5]))






