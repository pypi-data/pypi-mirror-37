# -*- coding: UTF-8 -*-
import random
import sys
import threading
import time

sys.path.append(r'../../')

import requests
from threadpool import ThreadPool, makeRequests

from oyospider.common.proxy_ip_pull import ProxyIpExtractHelper
import redis
from redis import ConnectionError
from scrapy.utils.project import get_project_settings


class RedisIPHelper(object):
    def __init__(self):
        settings = get_project_settings()
        host = settings.get('REDIS_HOST', '')
        port = settings.get('REDIS_PORT')
        password = settings.get('REDIS_PASSWORD')
        self.dailiyun_username = settings.get('DAILIYUN_USERNAME')
        self.dailiyun_password = settings.get('DAILIYUN_PASSWORD')

        try:
            self.redis_con = redis.StrictRedis(host=host, port=port, password=password)
        except NameError:
            return {'error': 'cannot import redis library'}
        except ConnectionError as e:
            return {'error': str(e)}

    def get_redis_ip(self):
        r = self.redis_con
        keys = r.keys("yunIps_*")
        # print(keys)
        if keys:
            IPs = []
            for key in keys:
                proxy_ip = r.get(key)
                # print key
                # print proxy_ip
                IPs.append(proxy_ip)

            return IPs
        else:
            return ""

    def load_usable_proxy_ip_to_redis(self, target_site, target_url):
        """
        加载可用的代理IP
        :param target_site:
        :param target_url:
        :return:
        """
        ip_helper = ProxyIpExtractHelper()
        ip_list = ip_helper.get_from_dailiyun()
        # 加载到redis中
        self.get_all_proxy_ip_usable(target_site, target_url, "dailiyun", ip_list,
                                     self.put_proxy_to_redis_pool)

    def callback_test(self, request, result):
        print("callback_test")

    def put_proxy_to_redis_pool(self, protocol, ip, port, source, target_site, batchno, expire_time):
        """
        将可用的meituan代理IP放入内存中
        :param protocol:
        :param ip:
        :param port:
        :param source:
        :param target_site:
        :param batchno:
        :param expire_time
        :return:
        """
        key = "proxy_ip_pool:%s:%s|%s|%s|%s" % (target_site, source, protocol, ip, port)
        self.redis_con.set(key, "")
        self.redis_con.expire(key, expire_time)

    def get_all_proxy_ip_usable(self, target_site, target_url, source, ip_list, put_proxy_to_redis):
        """
          测试指定URL代理的有效性

        """
        # useable_ip_list = []
        batchno = int(round(time.time() * 1000))
        # timestamp = int(round(time.time()))
        par_list = []
        for proxy_ip in ip_list:
            paras = []
            paras.append(proxy_ip)
            paras.append(target_site)
            paras.append(target_url)
            paras.append(source)
            paras.append(batchno)
            paras.append(put_proxy_to_redis)

            par_list.append((paras, None))
            # print paras
        print(" par_list = " + str(par_list))

        pool = ThreadPool(20)
        requests = makeRequests(self.test_proxy_ip_useable, par_list, self.callback_test)
        for req in requests:
            pool.putRequest(req)
        pool.wait()

    def test_proxy_ip_useable(self, ip_str, target_site, target_url, source, batchno, put_proxy_to_redis):
        """
        测试指定URL代理的有效性
      """

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

        ip_info = ip_str.split(",")
        ip_port = ip_info[0]
        protocol = "http"
        ip_addr = ip_port.split(":")[0]
        port = ip_port.split(":")[1]
        ip_effect_time = ip_info[3]
        ip_expire_time = int(ip_info[4])

        # 当前时间
        cur_timestamp = int(round(time.time())) + 5
        # 计算Ip的过期时间
        redis_expire_time = ip_expire_time - cur_timestamp
        print("ip_expire_time = %s,redis_expire_time = %s" % (ip_expire_time, redis_expire_time))
        user_name = self.dailiyun_username
        password = self.dailiyun_password
        proxy_url = "%s://%s:%s@%s:%s" % (protocol, user_name, password, ip_addr, port)

        proxy_obj = requests.utils.urlparse(proxy_url)

        test_url = target_url
        test_proxies = {
            "http": proxy_obj.netloc
        }
        if redis_expire_time > 0:
            # 测试代理有效性
            try:
                print("proxy:'%s',test_url:'%s'" % (proxy_url, test_url))
                response = requests.head(test_url, headers=headers, proxies=test_proxies, timeout=8)
                print("proxy:'%s',test_url:'%s',status_code:'%s'" % (test_proxies, test_url, response.status_code))
                if response.status_code == 200:
                    # return proxy_ip
                    if put_proxy_to_redis:
                        print("put_proxy_to_redis:%s,%s,%s,%s" % (protocol, ip_addr, port, redis_expire_time))
                        put_proxy_to_redis(protocol, ip_addr, port, source, target_site, batchno, redis_expire_time)
                    return proxy_url

            except Exception as e:
                print(e)
            else:
                return None


if __name__ == '__main__':
    redis_helper = RedisIPHelper()

    ctrip_thread = threading.Thread(target=redis_helper.load_usable_proxy_ip_to_redis,
                                    args=("ctrip", "https://hotels.ctrip.com/hotel/428365.html",))
    ctrip_thread.start()

    meituan_thread = threading.Thread(target=redis_helper.load_usable_proxy_ip_to_redis,
                                      args=("meituan", "https://www.meituan.com/jiudian/157349277/",))
    meituan_thread.start()
