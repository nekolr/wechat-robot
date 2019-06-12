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

weather_template_v1 = Template("$hello啊，兔子🐰！" + os.linesep +
                               os.linesep + "今天是 $date" + os.linesep +
                               os.linesep + "下面为你播报$city的天气🌡️" + os.linesep +
                               "今天白天$day_wea，有$day_win💨 $day_win_speed，最高气温为 $high" + os.linesep +
                               "今天晚间$night_wea，有$night_win💨 $night_win_speed，最低气温为 $low" + os.linesep + os.linesep)
