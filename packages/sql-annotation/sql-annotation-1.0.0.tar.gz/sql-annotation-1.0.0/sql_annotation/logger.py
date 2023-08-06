#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time           : 18-10-30 下午4:52
# @Author         : Tom.Lee
# @File           : logger.py
# @Product        : PyCharm
# @Docs           : 
# @Source         : 

import logging

logger = logging.getLogger('sql_annotation')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
