# -*- coding: UTF-8 -*-
import random
import sys
import threading

sys.path.append(r'../../')
import redis
from redis import ConnectionError
from scrapy.utils.project import get_project_settings

from oyospider.common.proxy_ip_oper import ProxyIPHelper
from oyospider.common.proxy_ip_pull import ProxyIpExtractHelper
import gevent.monkey

gevent.monkey.patch_all()


class RedisHelper(object):
    def __init__(self):
        settings = get_project_settings()
        host = settings.get('REDIS_HOST', '')
        port = settings.get('REDIS_PORT')
        password = settings.get('REDIS_PASSWORD')
        self.dailiyun_username = settings.get('DAILIYUN_USERNAME')
        self.dailiyun_password = settings.get('DAILIYUN_PASSWORD')
        # self.pool = Pool(1)

        # password = settings.get("REDIS_PARAMS").get('password')
        try:
            self.redis_con = redis.StrictRedis(host=host, port=port, password=password)
            # ping = self.ping()
        except NameError:
            return {'error': 'cannot import redis library'}
        except ConnectionError as e:
            return {'error': str(e)}

    def get_redis_conn(self):
        return self.redis_con

    def put_proxy_to_redis_pool(self, protocol, ip, port, source, target_site, batchno, expire_time):
        """
        将可用的代理IP放入redis池中
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

    def put_proxy_ip_to_redis_queue(self, protocol, ip, port, source, target_site, batchno, expire_time):
        """
        将可用的代理IP放入redis队列中
        :param protocol:
        :param ip:
        :param port:
        :param source:
        :param target_site:
        :param batchno:
        :param expire_time
        :return:
        """
        key = "proxy_ip_queue:%s:%s|%s|%s|%s" % (target_site, source, protocol, ip, port)
        self.redis_con.set(key, "")
        self.redis_con.expire(key, expire_time)

    def put_proxy_ip_to_redis_queue(self, targer_site, proxy_ip_str):
        """
        将可用的代理IP放入redis队列中
        :param targer_site:
        :param proxy_ip_str:
        :return:
        """
        key = "proxy_ip_queue:%s" % targer_site
        self.redis_con.rpush(key, proxy_ip_str)
        self.redis_con.expire(key, 60 * 10)

    def load_repeat_proxy_ip_ctrip(self):
        name = "ctrip_ip"
        proxy = self.redis_con.lpop(name)
        return proxy

    def load_repeat_proxy_ip_meituan(self):
        name = "meituan_ip"
        proxy = self.redis_con.lpop(name)
        return proxy

    def load_usable_proxy_ip_to_redis(self, target_site, target_url):
        """
        加载可用的代理IP
        :param target_site:
        :param target_url:
        :return:
        """
        # 加载到redis中
        # print"============ load_usable_proxy_ip_to_redis init============="
        proxy_ip_helper = ProxyIPHelper()

        proxy_ip_helper.get_all_proxy_ip_useable(target_site, target_url,
                                                 self.put_proxy_to_redis_pool)

    def get_usable_proxy_ip(self, site):
        """
        获得可以用的代理IP，没有的话直接从数据库里拿最近的代理IP，同时加载可用的代理IP到redis中
        :param site:
        :return:
        """
        # 判断redis中是否有代理
        # print "len = %s" % len(self.redis_con.sscan_iter(site + "_Ips"))

        site_keys = []
        print "get ip from redis "
        for key in self.redis_con.keys(site + "Ips*"):
            site_keys.append(key)
        print "redis keys = " + str(site_keys)
        if site_keys:
            site_ips = self.redis_con.srandmember(max(site_keys))
            if site_ips:
                return site_ips.split("|")
                # print site_ips(0)
                # print random.choice(site_ips)

        proxy_ip_helper = ProxyIPHelper()
        china_proxy_ips = proxy_ip_helper.find_china_proxy_ip(100)

        if china_proxy_ips:
            # 异步加载到redis中
            # self.pool.apply_async(self.load_usable_proxy_ip_to_redis, args=(site,))
            thread = threading.Thread(target=self.load_usable_proxy_ip_to_redis, args=(site,))
            # thread.setDaemon(True)
            thread.start()
            thread.join()
            # 先返回表中随机IP给调用者
            return random.choice(china_proxy_ips)
        else:
            return None

    def get_database_proxy_ip(self):
        p_ip = ProxyIpExtractHelper()
        p_ip.get_all_proxy_site()

    def get_usable_proxy_ip_from_redis_queue(self, target_site):
        """
        从队列中取代理ip
        :param target_site:
        :return:格式：代理来源|代理协议|代理IP|代理port
        """
        key = "proxy_ip_queue:%s" % target_site
        proxy_ip_queue = self.redis_con.lpop(key)
        print "get_usable_proxy_ip_from_redis_queue,proxy_ip = %s" % proxy_ip_queue
        return proxy_ip_queue

    def get_usable_proxy_ip_from_redis_pool(self, target_site):
        """
        从ip池中取代理ip
        :param target_site:
        :return:格式：代理来源|代理协议|代理IP|代理port
        """
        # 代理云数量相对西瓜代理数量较少，需要增加代理云的随机选中机率
        # 查询西代理IP数量
        random_key = ["dailiyun|*", "xiguadaili|*", "*"]
        sub_key = random.choice(random_key)
        match_key = "proxy_ip_pool:%s:%s" % (target_site, sub_key)
        print "match_key = %s" % match_key
        # print "get_usable_proxy_ip_from_redis_pool = %s" % match_key
        site_keys = []
        for key in self.redis_con.keys(match_key):
            site_keys.append(key)
        # print "get_usable_proxy_ip_from_redis_pool size :%s " % len(site_keys)
        proxy_ip_pool = None
        if len(site_keys) > 0:
            proxy_ip_key = random.choice(site_keys)
            proxy_ip_pool = proxy_ip_key.split(":")[2]
        print "get_usable_proxy_ip_from_redis_pool,proxy_ip = %s" % proxy_ip_pool
        return proxy_ip_pool

    def get_usable_proxy_ip_from_db(self):
        """
        从数据库中取代理ip
        :return:格式：代理来源|代理协议|代理IP|代理port
        """
        proxy_ip_helper = ProxyIPHelper()
        china_proxy_ips = proxy_ip_helper.find_all_proxy_ip()
        proxy_ip_recrod = random.choice(china_proxy_ips)
        proxy_ip_db = None
        if proxy_ip_recrod:
            proxy_ip_db = "%s|%s|%s|%s" % (
                proxy_ip_recrod[3], proxy_ip_recrod[0], proxy_ip_recrod[1], proxy_ip_recrod[2])
        print "get_usable_proxy_ip_from_db,proxy_ip = %s" % proxy_ip_db
        return proxy_ip_db

    def get_usable_proxy_ip_v2(self, target_site):
        """
       根据优先级获取可用ip
       :return:格式：代理来源|代理协议|代理IP|代理port
        """
        # 1.从队列中取 ip
        proxy_ip_str = self.get_usable_proxy_ip_from_redis_queue(target_site)
        if not proxy_ip_str:
            # 如果队列中有代理IP，则使用队列中的ip，如果没有，则从ip池中取
            # 2.从IP池中取 ip
            #
            proxy_ip_str = self.get_usable_proxy_ip_from_redis_pool(target_site)
        if not proxy_ip_str:
            # 3.从数据库中取ip
            proxy_ip_str = self.get_usable_proxy_ip_from_db()
        return proxy_ip_str

    def get_usable_request_proxy_ip(self, target_site):
        """
       获得可直接用于设置的代理IP
       :return:格式：scrapy resquest标准格式，可以直接使用，其它格式需要处理
        """
        proxy_ip_str = self.get_usable_proxy_ip_v2(target_site)
        proxy_ip_req = None
        if proxy_ip_str:
            # 根据代理来源判断生成代理ip的正确字符串
            proxy_ip_info = proxy_ip_str.split("|")
            proxy_source = proxy_ip_info[0]
            if proxy_source == "dailiyun":
                user_name = self.dailiyun_username
                password = self.dailiyun_password
                proxy_ip_req = "%s://%s:%s@%s:%s" % (
                    proxy_ip_info[1], user_name, password, proxy_ip_info[2], proxy_ip_info[3])
            elif proxy_source == "xiguadaili":
                proxy_ip_req = "%s://%s:%s" % (proxy_ip_info[1], proxy_ip_info[2], proxy_ip_info[3])
            else:
                print "unkown proxy_source:" + target_site
        return proxy_ip_req, proxy_ip_str


if __name__ == '__main__':
    redis_helper = RedisHelper()

    ctrip_thread = threading.Thread(target=redis_helper.load_usable_proxy_ip_to_redis,
                                    args=("ctrip", "https://hotels.ctrip.com/hotel/428365.html",))
    ctrip_thread.start()

    meituan_thread = threading.Thread(target=redis_helper.load_usable_proxy_ip_to_redis,
                                      args=("meituan", "https://www.meituan.com/jiudian/157349277/",))
    meituan_thread.start()

    ip_thread = threading.Thread(target=redis_helper.get_database_proxy_ip)
    ip_thread.start()
