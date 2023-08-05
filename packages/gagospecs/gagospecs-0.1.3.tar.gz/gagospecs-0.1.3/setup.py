#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-18


from distutils.core import setup

setup(
    name='gagospecs',
    version='0.1.3',
    description='Gago Specs Lib',
    author='Dajiang Ren',
    author_email='rendajiang@gagogroup.cn',
    url='http://www.gagogroup.cn',
    packages=[
        'gagospecs',
        'gagospecs.base',
        'gagospecs.v1',
        'gagospecs.v1.base',
        'gagospecs.v1.converters',
        'gagospecs.v1.generators',
        'gagospecs.v1.generators.original',
        'gagospecs.v1.models',
        'gagospecs.v1.models.original',
        'gagospecs.v1.converters',
        'gagospecs.v1.converters.original',
        'gagospecs.v1.schemas',
        'gagospecs.v1.schemas.original',
        'gagospecs.v1.services',
        'gagospecs.v1.validators',
        'gagospecs.v1.validators.original',
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
