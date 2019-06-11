#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from string import Template
import os

"""
天气模板
# 今天是 2019-6-11 星期二
# 北京的天气：晴
# 最高气温 32 ℃
# 最低气温 16 ℃
# 空气质量：良好
# 有东南风 3-4级转<3级
"""
weather_template = Template("今天是 $date $week" + os.linesep +
                            "$city：$wea" + os.linesep +
                            "最高气温：$high" + os.linesep +
                            "最低气温：$low" + os.linesep +
                            "空气质量：$quality" + os.linesep +
                            "有$win $win_speed" + os.linesep)
