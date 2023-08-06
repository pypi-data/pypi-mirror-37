#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time           : 18-10-30 下午4:32
# @Author         : Tom.Lee
# @File           : error.py
# @Product        : PyCharm
# @Docs           : 
# @Source         : 


class SQLAnnotationError(Exception):
    def __init__(self, code=500, msg='error!'):
        self.message = msg
        self.code = code


class DatabaseConnectionError(Exception):
    def __init__(self, code=500, msg=None):
        self.message = msg or "数据库连接失败"
        self.code = code
