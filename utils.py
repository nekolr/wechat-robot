#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from simplejson import JSONDecodeError
import itchat
import os
import logging


def is_json(response):
    """
    判断数据能否解析成 Json 格式
    :param response:
    :return:
    """
    try:
        response.json()
        return True
    except JSONDecodeError:
        return False


def get_json(response):
    """
    获取 json
    :param response:
    :return:
    """
    if response.status_code == 200 and is_json(response):
        return response.json()
    else:
        logging.warning('获取信息失败')


def is_online(auto_login=False):
    """
    判断是否还在线。
    :param auto_login: bool，如果掉线了则自动登录（默认为 False）
    :return:
    """

    def _online():
        """
        通过获取好友信息，判断用户是否还在线
        :return:
        """
        try:
            if itchat.search_friends():
                return True
        except IndexError:
            return False
        return True

    if _online():
        return True
    # 仅仅判断是否在线
    if not auto_login:
        return _online()

    # 尝试登录 5 次
    for _ in range(5):
        login()
        if _online():
            logging.info('登录成功')
            return True
    logging.info('登录成功')
    return False


def login():
    """
    登录微信
    :return:
    """
    # 命令行显示登录二维码
    if os.environ.get('MODE') == 'server':
        itchat.auto_login(enableCmdQR=2, hotReload=True)
    else:
        itchat.auto_login(hotReload=True)
