#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:j_li@ruijie.com.cn
@time: 2018/11/1 17:35
@desc:

"""
from distutils.core import setup
setup(name='skylineAlgorithms',
      version='1.0',
      description='Skyline Algorithms part',
      author='j_li',
      py_modules=['skyline'],
      install_requires=['numpy', 'pandas', 'scipy'],
      python_requires='>=3'
     )
