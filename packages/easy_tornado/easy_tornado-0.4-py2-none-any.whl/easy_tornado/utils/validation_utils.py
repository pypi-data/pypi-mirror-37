# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018年8月23日 14:26:49
from six.moves import xrange


# 检测字典data中是否包含指定的所有键
def contain_keys(_data, _keys):
    for _key in _keys:
        if _key not in _data:
            return False
    return True


# 检测数字是否在范围内
def in_range(_num, _range_from, _range_to):
    return _num in xrange(_range_from, _range_to + 1)
