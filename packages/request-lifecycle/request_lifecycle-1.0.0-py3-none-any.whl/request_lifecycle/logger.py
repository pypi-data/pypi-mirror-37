# Copyright 2018 Frank Lin. All Rights Reserved.
# -*- coding: utf-8 -*-

import requests
from typing import Dict, List


class RequestLifecycleLogger(object):
    """日志链路追加工具
    """

    def __init__(self, host: str, port: str, app_name: str, additional_req_field: List[str]):
        self.host = host
        self.port = port
        self.app_name = app_name
        self.additional_req_fields = additional_req_field

    def config(self, host: str, port: str, app_name: str, additional_req_field: List[str]) -> None:
        self.host = host
        self.port = port
        self.app_name = app_name
        self.additional_req_fields = additional_req_field

    def send_log(self, level: str, message: Dict, meta: Dict) -> None:
        url = 'http://%s/log:%s' % (self.host, self.port)

        data = {
            'appName': self.app_name,
            'message': message,
            'meta': meta,
            'level': level
        }

        requests.post(url=url, json=data, timeout=2)


request_lifecycle_logger = RequestLifecycleLogger(host='', port='', app_name='', additional_req_field=[])
