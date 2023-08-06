# Copyright 2018 Frank Lin. All Rights Reserved.
# -*- coding: utf-8 -*-

"""时间函数相关
"""
import time


def current_mills() -> int:
    """当前的时间，单位为毫秒
    """
    return int(round(time.time() * 1000))
