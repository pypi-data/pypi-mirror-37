# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018年8月23日 14:26:49
import hashlib
import json


# 获取文本的MD5值
def md5sum(text):
    _ctx = hashlib.md5()
    _ctx.update(text.encode('utf-8'))
    return _ctx.hexdigest()


# 将json字符串解析为dict
def parse_json(json_str):
    return json.loads(json_str)
