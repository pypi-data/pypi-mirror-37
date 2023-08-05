# -*- coding: UTF-8 -*-
import datetime
import json
import sys
import time
import urllib2

sys.path.append(r'../../')

from oyospider.common.db_operate import MySQLdbHelper

reload(sys)
sys.setdefaultencoding('utf-8')


def send_monitor_info():
    db_helper = MySQLdbHelper()

    sql = """
    SELECT
        ht.ota_name,
        ht.ota_hotel_count,
        tp.hotel_crawl_count,
        room_price_count,
        DATE_FORMAT(begin_time,'%%Y-%%m-%%d %%H:%%i') begin_time,
        DATE_FORMAT(end_time,'%%Y-%%m-%%d %%T') end_time,
        DATE_FORMAT(checkin_date,'%%Y-%%m-%%d') checkin_date,
        batch_no
    FROM
        (
        SELECT
            h.ota_name,
            count( 1 ) ota_hotel_count 
        FROM
            dm_hotel_monitor_ota_map_t h 
        WHERE
            h.ota_hotel_url <> '' 
            AND h.ota_hotel_url <> '/' 
        GROUP BY
            h.ota_name 
        ) ht
        INNER JOIN (
        SELECT
            t.ota_name,
            count( DISTINCT t.ota_hotel_id ) hotel_crawl_count,
            count( 1 ) room_price_count,
            min( create_time ) begin_time,
            max( create_time ) end_time,
            t.checkin_date,
            t.batch_no  batch_no
        FROM
            hotel_room_price_monitor t 
        WHERE
            t.create_time >= '%s'
            AND t.create_time < '%s' 
        GROUP BY
            t.ota_name,
            t.checkin_date,
            DATE_FORMAT( t.create_time, '%%Y-%%m-%%d %%H' ) 
        ORDER BY
            t.ota_name 
        ) tp 
    WHERE
        ht.ota_name = tp.ota_name and ht.ota_name = '%s'
    order by ota_name ,batch_no desc
    """
    end_time = datetime.datetime.strptime(time.strftime('%Y-%m-%d %H', time.localtime(time.time())) + ":59:59",
                                          "%Y-%m-%d %H:%M:%S")
    end_time_str = datetime.datetime.strftime(end_time, "%Y-%m-%d %H:%M:%S")
    begin_time_str = datetime.datetime.strftime(end_time + datetime.timedelta(hours=-3), "%Y-%m-%d %H:%M:%S")

    send_url = "https://oapi.dingtalk.com/robot/send?access_token=3b0cb4f0d390d8b3d12d76c198d733c780ebc0532f876d9e7801c6ff011f3da1"

    for ota_name in ["ctrip", "meituan"]:
        record = db_helper.executeSql(sql % (begin_time_str, end_time_str, ota_name))
        msg_body = []
        hotel_count = 0
        for r in record:
            hotel_count = r[1]
            msg_body.append(
                " > ###### 爬取时间：%s \n\n  > ###### 入住日期：%s \n\n> ###### 酒店总数：%s \n\n > ###### 房价总数：%s \n\n ######  \n\n" % (
                    r[4], r[6], r[2], r[3]))

        head_msg = " #### 全网最低价项目 #### \n\n %s 最近三次爬取统计：\n\n ##### 映射酒店总数:%s \n\n ———————————————— \n\n " % (
            ota_name, hotel_count)
        head_msg = head_msg + "\n\n ———————————————— \n\n".join(msg_body)
        # 发送消息
        post_data = {'msgtype': 'markdown',
                     'markdown': {'title': '全网最低价',
                                  'text': head_msg}
                     }
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        req = urllib2.Request(url=send_url, headers=headers, data=json.dumps(post_data))
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        print res


def send_scrapy_log_info():
    print "test"


if __name__ == '__main__':
    send_monitor_info()
