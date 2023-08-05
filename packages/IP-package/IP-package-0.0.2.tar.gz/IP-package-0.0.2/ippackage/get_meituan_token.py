# -*- coding: utf-8 -*-
import json
import os
import re
import sys
import time

from redis import StrictRedis
from selenium import webdriver

sys.path.append(r'../../')

from oyospider.common.db_operate import MySQLdbHelper
from oyospider.items import Meituan_tokenItem
from oyospider.settings import REDIS_HOST, REDIS_PORT, PHANTOMJS_PATH, SERVICE_LOG_PATH, REDIS_PASSWORD


class MeiTuanTokenHelper(object):
    def __init__(self):
        mydb = MySQLdbHelper()
        # self.ipdb = ProxyIP()

        # 查出来要爬取的监控酒店
        sql = "select * from dm_hotel_monitor_ota_map_t h where h.ota_name = 'meituan' limit 5"
        records = mydb.executeSql(sql)
        urls = []

        for row in records:
            if row[5] != '/':
                urls.append(row[5])

        self.start_urls = urls

    def start_requests(self):
        item = Meituan_tokenItem()
        for url in self.start_urls:
            browser = webdriver.PhantomJS(PHANTOMJS_PATH,
                                          service_log_path=SERVICE_LOG_PATH)

            browser.get(url)
            har = str(json.loads(browser.get_log('har')[0]['message']))

            if len(re.findall(r"_token=(.+?)&", har)) > 0:
                token_str = re.findall(r"_token=(.+?)&", har)[0]
                item['meituan_token'] = token_str
                if 'meituan_token' in item:
                    sr = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD,
                                     db=15)
                    cur_timestamp = (int(round(time.time() * 1000)))
                    keys = "meituan_token:%s" % cur_timestamp

                    key = keys
                    expire_time = 240
                    value = item["meituan_token"]

                    sr.setex(key, expire_time, value)
                    # return item
                    print item
                continue


if __name__ == '__main__':
    # t = time.time()
    # print (int(round(t * 1000)))
    sp = MeiTuanTokenHelper()
    # while True:
    try:
        sp.start_requests()
        # 自动kill 使用cpu超过5分钟的 phantomjs 进程
        cmd = '''kill -9 `ps -aux|grep phantomjs|awk '{split($10,arr,":");if(arr[1]*60+arr[2]>5){print $2}}'`
                '''
        os.system(cmd)
        time.sleep(10)
    except Exception as e:
        print(e)
