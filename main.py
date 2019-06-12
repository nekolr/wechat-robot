#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itchat
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import template
from utils import (get_json, is_online, login, say_hello)
from config import config
import logging

# UserAgent
ua = UserAgent(path='fake_useragent_0.1.11.json')
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
    response = requests.get("http://wufazhuce.com/", headers={'User-Agent': ua.random})
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
        return template.weather_template.substitute(
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


def get_weather_v1(city):
    """
    获取天气信息
    :param city:
    :return:
    """
    logging.info('从『 http://www.nmc.cn 』获取天气信息')
    weather = get_json(requests.get('http://www.nmc.cn/f/rest/weather/' + city))
    if weather is not None:
        return template.weather_template_v1.substitute(
            hello=say_hello(),
            date=weather[0]['detail'][0]['date'],
            city=weather[0]['station']['city'],
            day_wea=weather[0]['detail'][0]['day']['weather']['info'],
            night_wea=weather[0]['detail'][0]['night']['weather']['info'],
            high=weather[0]['detail'][0]['day']['weather']['temperature'] + ' 度',
            low=weather[0]['detail'][0]['night']['weather']['temperature'] + ' 度',
            day_win=weather[0]['detail'][0]['day']['wind']['direct'],
            night_win=weather[0]['detail'][0]['night']['wind']['direct'],
            day_win_speed=weather[0]['detail'][0]['day']['wind']['power'],
            night_win_speed=weather[0]['detail'][0]['night']['wind']['power']
        )


def send_today_info():
    """
    发送当天的信息
    :return:
    """
    # 获取天气
    weather_info = get_weather_v1(config['city'])
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
