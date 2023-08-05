# -*- coding: utf-8 -*-
import time


def zip_default():
    # 格式化时间戳为标准格式
    nowday_time = time.strftime('%Y%m%d_default.zip', time.localtime(time.time()))
    # print(nowday_time)
    zip_ml = "zip -r %s ./default.log" % (nowday_time)
    print(zip_ml)
    return zip_ml


if __name__ == '__main__':
    zip_default()
