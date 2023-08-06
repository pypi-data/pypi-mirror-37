#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time           : 18-10-30 下午1:29
# @Author         : Tom.Lee
# @File           : __init__.py.py
# @Product        : PyCharm
# @Docs           : 
# @Product        : PyCharm
from functools import wraps

import annotation
import database


def cell(sql, sql_syntax):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with getattr(database, 'db') as _db:
                function = getattr(_db, sql_syntax)
                return function(getattr(database, 'parser_sql')(sql, **kwargs))

        return wrapper

    return decorator


setattr(annotation, 'cell', cell)
