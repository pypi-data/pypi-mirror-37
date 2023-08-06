# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018年8月23日 14:26:49
import json

from tornado.httpclient import AsyncHTTPClient
from tornado.web import RequestHandler, asynchronous

from easy_tornado.utils.log_utils import it_print
from easy_tornado.utils.time_utils import current_datetime
from easy_tornado.utils.time_utils import current_timestamp


class WebApplicationHandler(RequestHandler):
    # 错误信息
    error_mapper = dict()

    # 正常响应
    none = 0
    error_mapper[none] = 'none'

    # 无效请求(参数错误)
    invalid_request = 1001
    error_mapper[invalid_request] = 'request param is invalid'

    # 数据未找到
    not_found = 4004
    error_mapper[not_found] = 'not found'

    # 本系统错误
    system_error = 5002
    error_mapper[system_error] = 'system error'

    # 内部服务器错误
    internal_server = 5003
    error_mapper[internal_server] = 'internal server'

    # 调试模式
    debug = False

    # 作为后台进程运行
    daemon = True

    # 加载为json数据
    def load_request_data(self):
        try:
            params = json.loads(self.request.body)
            if self.debug:
                params['request_time'] = current_datetime()
                self.pretty_it_print(params)
            # 加入私有属性作为数据，否则params为空，被if not判断为真
            params['_timestamp'] = current_timestamp()
        except ValueError:
            return False
        return params

    # 转发请求
    @asynchronous
    def forward(self, url, data=None, callback=None, method='POST', timeout=3600):
        if callback is None:
            callback = self.response
        if data is None:
            data = {}
        data = json.dumps(data, ensure_ascii=False)
        client = AsyncHTTPClient()
        client.fetch(url, body=data, callback=callback, method=method, request_timeout=timeout)

    def success_response(self, data=None):
        self.error_response(self.none, self.error_mapper[self.none], data)

    def error_response(self, error_no=invalid_request, error_desc=None, data=None):
        res = data
        if not data:
            res = dict()
        res['errno'] = error_no
        if error_desc is None:
            error_desc = self.error_mapper[error_no]
        res['error'] = error_desc
        self.__json_response(res)

    def __json_response(self, data):
        if self.debug:
            data['response_time'] = current_datetime()
        self.__output_response(json.dumps(data, ensure_ascii=False))

    def __output_response(self, data):
        if self.debug:
            it_print(data)
        self.write(data)
        self.finish()

    # 默认响应处理器
    def response(self, response):
        try:
            if self.debug:
                it_print(response.body)
            result = json.loads(response.body)
        except ValueError:
            return self.error_response(error_no=self.system_error)
        return self.success_response(result)

    def data_received(self, chunk):
        pass

    @staticmethod
    def pretty_it_print(data):
        it_print(json.dumps(data, ensure_ascii=False))
