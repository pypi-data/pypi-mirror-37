#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time           : 18-10-30 下午4:18
# @Author         : Tom.Lee
# @File           : annotation.py
# @Product        : PyCharm
# @Docs           : 
# @Source         : 


def cell(*args):
    """　
    :param args:
    :return:
    """
    pass


def select(sql):
    return cell(sql, 'select')


def insert(sql):
    return cell(sql, 'persistent')


def update(sql):
    return cell(sql, 'persistent')


def delete(sql):
    return cell(sql, 'delete')
