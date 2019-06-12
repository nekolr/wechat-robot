#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import template
import requests
from utils import (get_json, say_hello)
import logging
from fake_useragent import UserAgent

# UserAgent
ua = UserAgent(path='fake_useragent_0.1.11.json')


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


def get_one_info_v1():
    """
    获取一言（随机版）
    :return:
    """
    logging.info('从『 https://api.imjad.cn/hitokoto/ 』获取一句格言')
    r = get_json(
        requests.get("https://api.imjad.cn/hitokoto/", params={"encode": "json"}, headers={'User-Agent': ua.random}))
    return r['hitokoto'] + " —— " + r['source']


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
    weather = get_json(requests.get('http://www.nmc.cn/f/rest/weather/' + city, headers={'User-Agent': ua.random}))
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
