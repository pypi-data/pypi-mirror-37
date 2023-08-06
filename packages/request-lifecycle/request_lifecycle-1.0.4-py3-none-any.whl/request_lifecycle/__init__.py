# Copyright 2018 Frank Lin. All Rights Reserved.
# -*- coding: utf-8 -*-

"""该 module 用于日志收集，中间件需配合 flask framework
"""

__version__ = '1.0.4'

from .logger import RequestLifecycleLogger, request_lifecycle_logger
from .request_lifecycle import RequestLifecycleMiddleware
