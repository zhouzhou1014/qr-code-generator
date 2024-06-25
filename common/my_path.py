#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time    : 2024/6/22 10:34
# @Author  : zhouzhou
# @File    : my_path.py
# @Software: PyCharm
import os

# 项目主目录
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 生成QRCodes的基本数据路径
BasicData_path = os.path.join(basedir, 'BasicData')
# 二维码生成存放路径
QRCodes_path = os.path.join(basedir, 'qrCodeData')
# logo图存放路径
logos_path = os.path.join(basedir,  'logo_path')

fonts_path = os.path.join(basedir, 'font_path')
