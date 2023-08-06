#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time           : 18-11-1 上午9:35
# @Author         : Tom.Lee
# @File           : setup.py
# @Product        : PyCharm
# @Docs           : 
# @Source         : 

from setuptools import setup, find_packages

setup(
    name='sql-annotation',
    version='1.0.0',
    author='liyuanjun',
    author_email='1123431949@qq.com',
    url='https://github.com/tomoncle/sql-annotation',
    description='Database Annotation, author liyuanjun',
    long_description=open("README.md").read(),
    license="MIT",
    install_requires=[
        'MySQL-python'
    ],
    packages=find_packages()
)
