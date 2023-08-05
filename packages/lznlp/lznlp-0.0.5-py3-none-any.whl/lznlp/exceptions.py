# -*- coding: utf-8 -*-
from requests.exceptions import HTTPError


class TaskNotFoundError(HTTPError):
    """任务不存在。"""


class TaskError(HTTPError):
    """分析任务出错。"""


class TimeoutError(Exception):
    """分析任务超时。"""
