# -*- coding: UTF-8 -*-
# from oyospider.common.db_operate import MySQLdbHelper
import random
import sys
import time

sys.path.append(r'../../')
import requests
from threadpool import ThreadPool, makeRequests

from oyospider.common.db_operate import MySQLdbHelper


class ProxyIPHelper(object):
    def __init__(self):
        self.proxy_ip_table = "dm_proxy_ip_t"
        self.mydb = MySQLdbHelper()

    def get_usable_proxy_ip(self):
        sql = "select * from dm_proxy_ip_t"
        records = self.mydb.executeSql(sql)
        for record in records:
            print("get_usable_proxy_ip=" + record[1])
        return records

    def get_usable_anon_proxy_ip(self):
        """获取可用的高匿 代理IP
           """
        sql = "SELECT * FROM dm_proxy_ip_t p WHERE p.anon LIKE '%高匿%' AND DATE_FORMAT( succTime, '%Y-%m-%d' ) = ( SELECT DATE_FORMAT( max( succTime ), '%Y-%m-%d' ) FROM dm_proxy_ip_t )"
        records = self.mydb.executeSql(sql)
        # for record in records:
        #     print record[1]
        return records

    def get_usable_anon_proxy_ip_str(self):
        records = self.get_usable_anon_proxy_ip()
        ip_port = []
        for t in records:
            ip_port.append("http://" + t[1] + ":" + t[2])
        return ip_port

    def find_all_proxy_ip(self):
        """
          查出所有代理IP

        """
        db_helper = MySQLdbHelper()
        # proxy_ip_list = db_helper.select("proxy_ip", fields=["protocol", "ip", "port"])
        # proxy_ip_list = db_helper.executeSql("select protocol,ip,port from proxy_ip where 1=1 limit 1")
        proxy_ip_list = db_helper.executeSql(
            "SELECT protocol,ip,port,source FROM proxy_ip as t order by t.id DESC limit 2000;")
        return proxy_ip_list

    def find_china_proxy_ip(self, limit):
        """
          查出中国境内代理IP，作为打底数据

        """
        db_helper = MySQLdbHelper()
        # proxy_ip_list = db_helper.select("proxy_ip", fields=["protocol", "ip", "port"])
        sql = "select protocol,ip,`port`,source from proxy_ip t where 1=1 and ( t.area like '%山东%' or t.area like '%江苏%' " \
              "or t.area like '%上海%' or t.area like '%浙江%' or t.area like '%安徽%' or t.area like '%福建%' or t.area like '%江西%' " \
              "or t.area like '%广东%' or t.area like '%广西%' or t.area like '%海南%' or t.area like '%河南%' or t.area like '%湖南%' " \
              "or t.area like '%湖北%' or t.area like '%北京%' or t.area like '%天津%' or t.area like '%河北%' or t.area like '%山西%' " \
              "or t.area like '%内蒙%' or t.area like '%宁夏%' or t.area like '%青海%' or t.area like '%陕西%' or t.area like '%甘肃%' " \
              "or t.area like '%新疆%' or t.area like '%四川%' or t.area like '%贵州%' or t.area like '%云南%' or t.area like '%重庆%' " \
              "or t.area like '%西藏%' or t.area like '%辽宁%' or t.area like '%吉林%' or t.area like '%黑龙%' or t.area like '%香港%' " \
              "or t.area like '%澳门%' or t.area like '%台湾%') order by t.create_time desc limit " + str(limit)
        proxy_ip_list = db_helper.executeSql(sql)
        return proxy_ip_list

    def callback_test(self, request, result):
        print("callback_test")

    def get_all_proxy_ip_useable(self, target_site, target_url, put_proxy_to_redis):
        """
          测试指定URL代理的有效性

        """
        proxy_ip_list = self.find_all_proxy_ip()
        # useable_ip_list = []
        batchno = int(round(time.time() * 1000))
        # timestamp = int(round(time.time()))
        par_list = []
        for proxy_ip in proxy_ip_list:
            paras = []
            paras.append(proxy_ip[0])
            paras.append(proxy_ip[1])
            paras.append(proxy_ip[2])
            paras.append(proxy_ip[3])
            paras.append(target_site)
            paras.append(target_url)
            paras.append(batchno)
            paras.append(put_proxy_to_redis)
            par_list.append((paras, None))
            # print paras
        print(par_list)

        pool = ThreadPool(50)
        requests = makeRequests(self.test_proxy_ip_useable1, par_list, self.callback_test)
        for req in requests:
            pool.putRequest(req)
        pool.wait()

        # for proxy_ip in proxy_ip_list:
        #     # protocol = proxy_ip[0]
        #     # ip = proxy_ip[1]
        #     # port = proxy_ip[2]
        #
        #     test_proxy_id = self.test_proxy_ip_useable(proxy_ip[0], proxy_ip[1], proxy_ip[2], target_url)
        #     print "proxy_ip = " + str(test_proxy_id)
        #     if test_proxy_id:
        #         put_proxy_to_redis(proxy_ip[0], proxy_ip[1], proxy_ip[2])
        #         useable_ip_list.append(test_proxy_id)
        #     # redis_helper
        # return useable_ip_list
        # redis_helper

    def test_proxy_ip_useable(self, protocol, ip, port, target_url):
        proxy = ""
        if protocol:
            proxy = protocol + "://" + ip + ":" + port
        else:
            proxy = "http://" + ip + ":" + port
            # proxy ="18017115578:194620chao@"+  ip + port
            # user_agent_list = RotateUserAgentMiddleware()
        user_agent_list = [ \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]

        headers = {
            "User-Agent": random.choice(user_agent_list)
        }
        proxy_obj = requests.utils.urlparse(proxy)

        if proxy_obj.scheme.upper() == 'HTTP':
            test_url = target_url
            test_proxies = {
                "http": proxy_obj.netloc
            }

        elif proxy_obj.scheme.upper() == 'HTTPS':
            test_url = target_url
            test_proxies = {
                "https": proxy_obj.netloc
            }
        if test_proxies:
            # 测试代理有效性
            try:
                print("proxy:'%s',test_url:'%s'" % (proxy, test_url))
                response = requests.head(test_url, headers=headers, proxies=test_proxies, timeout=8)
                print("proxy:'%s',test_url:'%s',status_code:'%s'" % (proxy, test_url, response.status_code))
                if response.status_code == 200:
                    # return proxy_ip
                    return protocol, ip, port

            except Exception as e:
                print(e)
        else:
            return None

    def test_proxy_ip_useable1(self, protocol, ip, port, source, target_site, target_url, batchno, put_proxy_to_redis):
        proxy = ""
        if protocol:
            proxy = protocol + "://" + ip + ":" + port
        else:
            proxy = "http://" + ip + ":" + port

            # user_agent_list = RotateUserAgentMiddleware()
        user_agent_list = [ \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]

        headers = {
            "User-Agent": random.choice(user_agent_list)
        }
        proxy_obj = requests.utils.urlparse(proxy)

        if proxy_obj.scheme.upper() == 'HTTP':
            test_url = target_url
            test_proxies = {
                "http": proxy_obj.netloc
            }

        elif proxy_obj.scheme.upper() == 'HTTPS':
            test_url = target_url
            test_proxies = {
                "https": proxy_obj.netloc
            }
        if test_proxies:
            # 测试代理有效性
            try:
                print("proxy:'%s',test_url:'%s',source:'%s'" % (proxy, test_url, source))
                response = requests.head(test_url, headers=headers, proxies=test_proxies, timeout=8)
                print("proxy:'%s',test_url:'%s',source:'%s',status_code:'%s'" % (
                    proxy, test_url, source, response.status_code))
                if response.status_code == 200:
                    # return proxy_ip
                    if put_proxy_to_redis:
                        print("put_proxy_to_redis:%s,%s,%s" % (protocol, ip, port))
                        put_proxy_to_redis(protocol, ip, port, source, target_site, batchno, 60 * 15)
                    return protocol, ip, port

            except Exception as e:
                print(e)
        else:
            return None
