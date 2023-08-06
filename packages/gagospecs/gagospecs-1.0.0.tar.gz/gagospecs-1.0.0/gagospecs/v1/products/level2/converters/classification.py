#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-07


from gagospecs.v1.base.converter import Converter


class ClassificationConverter(Converter):
    def __init__(self):
        super().__init__('classification')
