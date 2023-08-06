#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-18


from distutils.core import setup

setup(
    name='gagospecs',
    version='1.0.2',
    description='Gago Specs Lib',
    author='Dajiang Ren',
    author_email='rendajiang@gagogroup.cn',
    url='http://www.gagogroup.cn',
    packages=[
        'gagospecs',
        'gagospecs.base',
        'gagospecs.v1',
        'gagospecs.v1.base',
        'gagospecs.v1.products.level2.converters',
        'gagospecs.v1.products.level2.models',
        'gagospecs.v1.products.level2.schemas',
        'gagospecs.v1.products.level3.models',
        'gagospecs.v1.products.level3.schemas',
        'gagospecs.v1.services',
    ],
    requires=[
        'gdal',
        'marshmallow'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
