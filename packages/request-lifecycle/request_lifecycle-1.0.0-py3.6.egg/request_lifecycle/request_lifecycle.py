# Copyright 2018 Frank Lin. All Rights Reserved.
# -*- coding: utf-8 -*-

import socket
from typing import List
from flask import Flask, request
from flask import g
from uuid import uuid4
from .logger import request_lifecycle_logger
from request_lifecycle.time_util import current_mills


class RequestLifecycleMiddleware(object):
    """收集请求的中间件
    """

    @staticmethod
    def before_request(host: str, port: str, app_name: str, additional_req_fields: List[str]) -> None:
        g.trace_id = str(uuid4())
        g.created_at_in_mills = current_mills()
        request_lifecycle_logger.config(host=host, port=port, app_name=app_name,
                                        additional_req_field=additional_req_fields)

    @staticmethod
    def after_request(response: Flask.response_class) -> None:
        now = current_mills()
        duration = now - g.created_at_in_mills

        message = {
            'traceId': g.trace_id,
            'appName': request_lifecycle_logger.app_name,
            'host': socket.gethostname(),
            'request': {
                'ip': request.remote_addr,
                'originalUrl': request.url,
                'method': request.method,
                'body': request.data.decode('utf-8'),
                'files': request.files,
                'headers': request.headers.to_list('utf-8')
            },
            'response': {
                'headers': response.headers.to_list('utf-8'),
                'body': response.get_data().decode('utf-8'),
                'statusCode': response.status_code
            },
            'durationInMills': duration
        }

        request_lifecycle_logger.send_log(level='info', message=message, meta={})
