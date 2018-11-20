#! -*- coding:utf8 -*-


# 1. 请求
# 2. 解析
# 3. 下载
import datetime
import urllib.request
#
import pymysql
import requests
import re
from multiprocessing import Pool, pool
# # 特殊异常要先引入
from requests.exceptions import RequestException

def call_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_notes(html):
    patt = re.compile('<div class="padT12 centerFi marB10"><img src="(.*?)" alt="チャート画像"></div>',re.S)
    items = re.findall(patt,html)
    return items





if __name__ == '__main__':
    pool =Pool(4)

    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='JS',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cur = connection.cursor()
    #sql 语句
    for num in range(1,3600):
        big_list = []
        sql = 'select coding from js_infos where id = %s ' % num
        # #执行sql语句
        cur.execute(sql)
        # #获取所有记录列表
        data = cur.fetchone()
        num_coding = data['coding']
        url = 'https://stocks.finance.yahoo.co.jp/stocks/chart/?code=' + str(num_coding) + '.T&ct=z&t=2y&q=c&l=off&z=m&p=m65,m130,s&a=v'
        html = call_page(url)
        content = parse_notes(html)
        for item in content:
            urllib.request.urlretrieve(item, '/home/karson/JS_Pics/%s.jpg' % num_coding )
            print(datetime.datetime.now())
