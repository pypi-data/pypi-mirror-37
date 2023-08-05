# -*- coding: UTF-8 -*-
import re
import sys
import time

sys.path.append(r'../../')
import requests
from oyospider.common.db_operate import MySQLdbHelper


class ProxyIpExtractHelper(object):
    """
    从各网获取代理IP操作类
    """

    def get_from_xiguan(self, fetch_num):
        """
        西瓜代理提取接口，并入库
        接口文档：http://www.xiguadaili.com/api
          """
        for protocol in ["http", "https"]:
            if not fetch_num:
                fetch_num = "100"
            # protocol = "http"
            api_url = "http://api3.xiguadaili.com/ip/?tid=556077616504319&category=2&show_area=true&show_operator=true&num=%s&protocol=%s" % (
                fetch_num, protocol)
            # api_url = "http://dly.134t.com/query.txt?key=NPBF565B9C&word=&count=%s"%(fetch_num)
            # api_url = "http://svip.kdlapi.com/api/getproxy/?orderid=963803204081436&num=%s&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=2&method=2&an_an=1&an_ha=1&sep=1"%(fetch_num)
            print("get_from_xiguan url = " + api_url)
            proxy_ips = []
            response = requests.get(api_url)
            res = response.text
            # print res
            if res:
                ip_list = res.split("\r\n")

                field = ["ip", "port", "operator", "area", "protocol", "anon", "delay", "source", "type", "create_time"]
                values = []
                for ip_str in ip_list:
                    # print type(ip_str)
                    # print re.findall(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}", ip_str)[0]
                    # print ip_str
                    ip = re.findall(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}", ip_str)[0]
                    port = re.findall(r":(\d+).*", ip_str)[0]
                    area = ""
                    if re.findall(r"@(.*)#", ip_str):
                        area = re.findall(r"@(.*)#", ip_str)[0]
                    operator = ""
                    if re.findall(r"#(.*)", ip_str):
                        operator = re.findall(r"#(.*)", ip_str)[0]

                    # proxy_ip = ({"ip": ip, "port": port, "area": area, "operator": operator, "protocol": protocol})
                    value = []
                    value.append(ip)
                    value.append(port)
                    value.append(operator)
                    value.append(area)
                    value.append(protocol)
                    value.append("2")
                    value.append("")
                    value.append("xiguadaili")  # 代理IP来源
                    value.append("1")  # 收费
                    value.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                    values.append(value)
                    # print value
                    # print proxy_ip
                    # proxy_ips.append(proxy_ip)
                db_helper = MySQLdbHelper()
                # 插入临时表
                db_helper.insertMany("proxy_ip_swap", field, values)
                # 插入正式表，用于去重
                insert_sql = "insert into proxy_ip(ip,port,operator,area,protocol,anon,delay,source,type,create_time) select ip,port,operator,area,protocol,anon,delay,source,type,create_time from proxy_ip_swap s where not exists (select null from proxy_ip p where p.ip = s.ip and p.port = s.port and p.protocol = s.protocol)"

                db_helper.executeCommit(insert_sql)

        return proxy_ips

    def get_from_dailiyun(self):
        """
        代理云提取接口，直接入redist
        接口文档：https://www.showdoc.cc/bjt5521?page_id=157160154849769
          """
        # api_url = "http://dly.134t.com/query.txt?key=NPBF565B9C&word=&count=1000"
        api_url = "http://dly.134t.com/query.txt?key=NPBF565B9C&word=&count=100&detail=true"
        print("get_from_dailiyun url = " + api_url)
        response = requests.get(api_url)
        res = response.text
        if res:
            ip_list = res.split("\r\n")
            return ip_list

    def get_all_proxy_site(self):
        """
          从网站或API获得所有代理IP

        """
        print("get_all_proxy_site")
        db_helper = MySQLdbHelper()
        # 1.西瓜代理
        self.get_from_xiguan(1000)

        # 清空临时表
        truncate_sql = "truncate table proxy_ip_swap"
        db_helper.executeCommit(truncate_sql)


# print proxy_ip["ip"] + "," + proxy_ip["port"] + "," + proxy_ip["area"] + "," + proxy_ip[
#         "operator"] + "," + proxy_ip["protocol"]
# for ip_str in range(5):
#     print proxy_ip["ip"] + "," + proxy_ip["port"] + "," + proxy_ip["area"] + "," + proxy_ip[
#         "operator"] + "," + proxy_ip["protocol"]


if __name__ == '__main__':
    # str = "61.222.87.87:38157@台湾省#电信"
    # print re.findall(r":(\d+).*", str)[0]
    # print re.findall(r"@(.*)#", str)[0]
    # print re.findall(r"#(.*)", str)[0]
    #
    # print re.findall(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}", str)[0]

    extract_helper = ProxyIpExtractHelper()
    extract_helper.get_all_proxy_site()
    # adapter.get_all_proxy_site()
    # adapter.test_proxy_ip_useable("hotel.meituan.com/shanghai/")
    # adapter.load_usable_proxy_ip_to_redis("meiTuan")
