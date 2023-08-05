# -*- coding: UTF-8 -*-
import sys
import threading
import time

import schedule

sys.path.append(r'../../')
from oyospider.common.get_meituan_token import MeiTuanTokenHelper
from oyospider.common.proxy_ip_pull_redis import RedisIPHelper
from oyospider.common.redis_operate import RedisHelper


def get_all_proxy_to_db_and_redis_job():
    redis_helper = RedisHelper()

    ctrip_thread = threading.Thread(target=redis_helper.load_usable_proxy_ip_to_redis,
                                    args=("ctrip", "https://hotels.ctrip.com/hotel/428365.html",))
    ctrip_thread.start()

    meituan_thread = threading.Thread(target=redis_helper.load_usable_proxy_ip_to_redis,
                                      args=("meituan", "https://www.meituan.com/jiudian/157349277/",))
    meituan_thread.start()

    ip_thread = threading.Thread(target=redis_helper.get_database_proxy_ip)
    ip_thread.start()


def get_dailiyun_proxy_to_redis_job():
    redis_helper = RedisIPHelper()
    ctrip_thread = threading.Thread(target=redis_helper.load_usable_proxy_ip_to_redis,
                                    args=("ctrip", "https://hotels.ctrip.com/hotel/428365.html",))
    ctrip_thread.start()

    meituan_thread = threading.Thread(target=redis_helper.load_usable_proxy_ip_to_redis,
                                      args=("meituan", "https://www.meituan.com/jiudian/157349277/",))
    meituan_thread.start()


def get_meituan_token():
    meituan_helper = MeiTuanTokenHelper()
    meituan_token_thread = threading.Thread(target=meituan_helper.start_requests)
    meituan_token_thread.start()


if __name__ == '__main__':
    try:
        get_all_proxy_to_db_and_redis_job()
        get_dailiyun_proxy_to_redis_job()
        get_meituan_token()
        #
        schedule.every(10).minutes.do(get_all_proxy_to_db_and_redis_job)
        schedule.every(2).minutes.do(get_dailiyun_proxy_to_redis_job)
        schedule.every(20).seconds.do(get_meituan_token)
    except Exception as e:
        print(e)
    #
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            print(e)
    # num = [1, 3, 6, 4, 2, ]
    # for i in range(3):
    #     print i, num[i]
