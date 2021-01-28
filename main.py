#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itchat
from apscheduler.schedulers.blocking import BlockingScheduler
from utils import (is_online, login)
from api import (get_one_info_v1, get_weather_v1)
from config import config
import logging

# 日志基本设置
logging.basicConfig(level=logging.INFO,
                    format=config['logging_format'])


def send_today_info():
    """
    发送当天的信息
    :return:
    """
    # 获取天气
    weather_info = get_weather_v1(config['city'])
    # 获取一言
    one_info = get_one_info_v1()

    if is_online(auto_login=True):
        # 获取好友列表
        itchat.get_friends(update=True)
        # 查找好友
        girl_friend = itchat.search_friends(name=config['girl_friend'])[0]
        # 发送消息
        itchat.send(weather_info + one_info, toUserName=girl_friend['UserName'])
    logging.info('发送成功')


def start():
    # 先登录一次，用于保存登录信息
    login()
    # 定时任务
    scheduler = BlockingScheduler()
    # 每天定时发送天气信息
    scheduler.add_job(send_today_info, 'cron', hour=config['hour'], minute=config['minute'],
                      misfire_grace_time=config['grace_time'])
    # 启动定时任务
    scheduler.start()


if __name__ == '__main__':
    start()
