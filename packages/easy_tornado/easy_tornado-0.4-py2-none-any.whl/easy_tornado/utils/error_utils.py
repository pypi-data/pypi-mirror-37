# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018年8月23日 14:26:49
from .log_utils import it_print


# 退出并打印消息
def error_exit(_error_no, _error_desc=None):
    if _error_desc:
        it_print(_error_desc)
    exit(_error_no)
