#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-17


from sys import modules


def create_module(
        name_space: str,
        product_level: str,
        product_type: str
):
    try:
        module_name: str = 'gagospecs.v1.' + \
                           name_space + \
                           '.' + \
                           product_level + \
                           '.' + \
                           product_type
        __import__(module_name)
        m = modules[module_name]
    except ImportError:
        m = None

    return m
