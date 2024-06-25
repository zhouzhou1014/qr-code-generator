#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time    : 2024/6/22 10:48
# @Author  : zhouzhou
# @File    : myConf.py
# @Software: PyCharm
from configparser import ConfigParser


class MyConf(ConfigParser):

    def __init__(self, filename):
        super().__init__()
        self.read(filename, encoding="utf-8")