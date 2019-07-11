# -*- coding: utf-8 -*-
"""
Created on Mon May 27 14:18:44 2019

@author: 张鹏举

import os
print os.path.dirname(os.path.realpath(__file__))


os.path.realpath

os.path.abspath    两者之间的区别

os.path.abspath()返回绝对路径，但不处理符号链接(注意linux中的符号链接不同于windows中的快捷方式)

os.path.realpath()先处理路径中的符号链接，再返回绝对路径
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/trait')
