#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itchat
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from template import weather_template
from utils import get_json, is_online
from config import config
import logging

# UserAgent
ua = UserAgent()
# 日志基本设置
logging.basicConfig(level=logging.INFO,
                    format=config['logging_format'])


def get_daily_sentence():
    """
    金山词霸每日一句
    :return:
    """
    logging.info('从『 http://open.iciba.com/dsapi/ 』获取金山词霸每日一句')
    return get_json(requests.get('http://open.iciba.com/dsapi/'))


def get_one_info():
    """
    从『一个。one』获取信息
    :return: str， 一句格言或者短语。
    """
    logging.info('从『 http://wufazhuce.com/ 』获取一句格言')
    response = requests.get("http://wufazhuce.com/", headers={'User-Agent': ua.chrome})
    if response.status_code == 200:
        soup_texts = BeautifulSoup(response.text, 'lxml')
        # 『one -个』 中的每日一句
        return soup_texts.find_all('div', class_='fp-one-cita')[0].find('a').text


def get_weather(city):
    """
    获取天气信息
    :return:
    """
    logging.info('从『 https://www.tianqiapi.com/api 』获取天气信息')
    weather = get_json(requests.get('https://www.tianqiapi.com/api', params={"version": "v1", "city": city}))
    if weather is not None:
        return weather_template.substitute(
            date=weather['data'][0]['date'],
            week=weather['data'][0]['week'],
            city=weather['city'],
            wea=weather['data'][0]['wea'],
            high=weather['data'][0]['tem1'],
            low=weather['data'][0]['tem2'],
            quality=weather['data'][0]['air_level'],
            win=weather['data'][0]['win'][0],
            win_speed=weather['data'][0]['win_speed']
        )


def send_today_info():
    """
    发送当天的信息
    :return:
    """
    # 获取天气
    weather_info = get_weather('通州')
    # 获取一言
    one_info = get_one_info()

    if is_online(auto_login=True):
        # 获取好友列表
        itchat.get_friends(update=True)
        # 查找好友
        girl_friend = itchat.search_friends(name=config['girl_fried'])[0]
        # 发送消息
        itchat.send(weather_info + one_info, toUserName=girl_friend['UserName'])
    logging.info('发送成功')


def start():
    # 定时任务
    scheduler = BlockingScheduler()
    # 每天定时发送天气信息
    scheduler.add_job(send_today_info, 'cron', hour=config['hour'], minute=config['minute'],
                      misfire_grace_time=config['grace_time'])
    # 启动定时任务
    scheduler.start()


if __name__ == '__main__':
    start()
