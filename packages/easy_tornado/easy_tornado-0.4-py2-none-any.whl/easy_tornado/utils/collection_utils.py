# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018/8/27 15:26
from collections import Iterable


# 获取无重复的列表
def unique_list(items):
    if not isinstance(items, Iterable):
        return items
    return list(set(items))
