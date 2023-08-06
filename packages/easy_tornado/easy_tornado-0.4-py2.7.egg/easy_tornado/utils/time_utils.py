# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018年8月23日 14:26:49
from __future__ import division

import time

from .log_utils import it_print


# 获取当前时间戳
def current_timestamp():
    return time.time()


# 获取当前日期
def current_datetime(_timestamp=None):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(_timestamp))


# 获取当前时间戳对应的日期时间
def current_datetime_str(_timestamp=None):
    return time.strftime("%Y%m%d%H%M%S", time.localtime(_timestamp))


# 获取当前时间戳对应的日期时间
def current_datetime_str_s(_timestamp=None):
    return time.strftime("%Y%m%dT%H%M%S", time.localtime(_timestamp))


# 计时器类
class Timer(object):
    # 无效时间戳标志
    _invalid_ts = -1

    def __init__(self, debug=False):
        self.debug = debug
        self._start_ts = self._invalid_ts
        self._finish_ts = self._invalid_ts
        self.reset()

    def reset(self):
        self.start()
        if self.debug:
            self.display_start('start at: ')

    @property
    def start_ts(self):
        return self._start_ts

    @property
    def finish_ts(self):
        return self._finish_ts

    def start(self):
        self._start_ts = time.time()
        self._finish_ts = self._invalid_ts

    def finish(self):
        self._finish_ts = time.time()

    def cost(self):
        self._set_finish()
        return self._finish_ts - self._start_ts

    def display_start(self, msg):
        Timer._display_datetime(self._start_ts, msg)

    def display_finish(self, msg):
        self._set_finish()
        Timer._display_datetime(self._finish_ts, msg)

    def display_cost(self, msg=None):
        cost = self.cost()
        prefix = ''
        if msg:
            prefix = 'Job [%s] ' % msg
        self.display_start(prefix + 'start at: ')
        self.display_finish(prefix + 'finished at: ')
        it_print('cost %d seconds' % cost)

    def _set_finish(self):
        if self._finish_ts == self._invalid_ts:
            self.finish()

    @staticmethod
    def _display_datetime(_ts, _msg):
        _tmp_msg = current_datetime(_ts)
        if _msg:
            if not _msg.endswith(' '):
                _msg += ' '
            _tmp_msg = _msg + _tmp_msg
        it_print(_tmp_msg)
