#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
配置文件
"""
config = {
    # 女朋友微信名称
    'girl_fried': u'nekolr',
    # 每天发送消息的时间 6 点 40 分
    'hour': '6',
    'minute': '40',
    # the time (in seconds) how much this job’s execution is allowed to be late
    'grace_time': 15 * 60,
    # 女朋友所在地
    'city': '通州',
    # 日志输出格式
    'logging_format': '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
}
