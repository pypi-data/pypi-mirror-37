#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time           : 18-10-31 下午6:50
# @Author         : Tom.Lee
# @CopyRight      : 2016-2017 OpenBridge by yihecloud
# @File           : conn.py
# @Product        : PyCharm
# @Docs           : 
# @Source         : 


import database
from .error import SQLAnnotationError


def connection(username, password, db, host='localhost', port=3306, driver='MYSQL'):
    """
    create db connection
    :param username: 　
    :param password:
    :param db:
    :param host:
    :param port:
    :param driver: database driver 
    :return:
    """
    if driver == 'MYSQL':
        database.db = database.MySQLUtils(
            host=host,
            port=port,
            user=username,
            passwd=password,
            db=db)

    else:
        raise SQLAnnotationError(
            msg='不支持{driver}数据库驱动连接'.format(driver=driver))
