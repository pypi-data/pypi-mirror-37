# Copyright 2018 Frank Lin. All Rights Reserved.
# -*- coding: utf-8 -*-

"""日志链路追加工具
"""
from typing import Dict, List
import requests


class RequestLifecycleLogger(object):
    """日志链路追加工具
    """

    def __init__(self, host: str, port: str, app_name: str, additional_req_field: List[str]):
        self.host = host
        self.port = port
        self.app_name = app_name
        self.additional_req_fields = additional_req_field

    def config(self, host: str, port: str, app_name: str, additional_req_field: List[str]) -> None:
        """配置 log-server 参数
        :param host: log-server 的 host
        :param port: log-server 的 port
        :param app_name: 自己的 app 的名字
        :param additional_req_field: 一些额外的需要追加的在 request 的 key (在目前的版本中无法使用)
        """
        self.host = host
        self.port = port
        self.app_name = app_name
        self.additional_req_fields = additional_req_field

    def send_log(self, level: str, message: Dict, meta: Dict) -> None:
        """发送日志到日志服务器
        :param level: 可以是 info 或者是 error
        :param message: 消息字典
        :param meta: 一些额外的消息字典
        """
        url = 'http://%s:%s/log' % (self.host, self.port)

        data = {
            'appName': self.app_name,
            'message': message,
            'meta': meta,
            'level': level
        }

        requests.post(url=url, json=data, timeout=2)


request_lifecycle_logger = RequestLifecycleLogger(host='', port='', app_name='', additional_req_field=[])
