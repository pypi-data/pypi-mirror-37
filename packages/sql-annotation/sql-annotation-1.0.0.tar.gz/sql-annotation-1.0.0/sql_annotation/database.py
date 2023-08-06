#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time           : 18-11-1 上午9:41
# @Author         : Tom.Lee
# @File           : database.py
# @Product        : PyCharm
# @Docs           : 
# @Source         : 
from contextlib import closing

import MySQLdb

from .error import DatabaseConnectionError
from .logger import logger


class Database(object):
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

        self.args = args
        self.kwargs = kwargs

    def select(self, *args, **kwargs):
        raise NotImplementedError

    def persistent(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError


class _Closing(closing):
    def __exit__(self, *exc_info):
        if self.thing:
            self.thing.close()


class MySQLUtils(Database):
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

        if not kwargs.get('charset'):
            kwargs['charset'] = 'utf8'
        super(MySQLUtils, self).__init__(*args, **kwargs)
        self.__connection = None
        self.__cursor = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        if exc_tb:
            logger.error('[%s]%s' % (exc_type, exc_val))

    def open(self):
        if self.__connection:
            raise MySQLdb.MySQLError("connection already connected.")
        try:
            self.__connection = MySQLdb.connect(*self.args, **self.kwargs)
        except Exception:
            logger.error("数据库连接异常, 请设置：sql_annotation.conn.connection 的连接信息.")
            raise DatabaseConnectionError

        if self.__cursor:
            raise MySQLdb.MySQLError("cursor already opened.")
        self.__cursor = self.__connection.cursor(MySQLdb.cursors.DictCursor)
        # logger.info("connection opened.")

    def close(self):
        with _Closing(self.__cursor) as _:
            pass
        with _Closing(self.__connection) as _:
            pass
        self.__cursor = None
        self.__connection = None
        # logger.info("connection close success.")

    def __execute(self, sql, commit=False):
        if not (self.__connection and self.__cursor):
            raise MySQLdb.MySQLError("connection already closed.")
        count = self.__cursor.execute(sql)
        result = self.__cursor.fetchall()
        self.__connection.commit() if commit else None
        return count if commit else result

    def select(self, sql, formatter_func=None):
        logger.info("Execute SQL: {}".format(sql))
        if formatter_func:
            return map(formatter_func, self.__execute(sql))
        return self.__execute(sql)

    def persistent(self, sql):
        return self.__execute(sql, True)

    def delete(self, sql):
        return self.__execute(sql, True)


def parser_sql(sql, **kwargs):
    for k, v in kwargs.items():
        number = "#{" + k + "}"
        if number in sql:
            sql = sql.replace(number, '{}'.format(v))
            continue

        string = "#{{" + k + "}}"
        if string in sql:
            sql = sql.replace(string, "'{}'".format(v))
    return sql
