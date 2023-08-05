#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-17


from gagospecs.v1.base.model import GMDModel


def post_load_object(obj: GMDModel, **kwargs):
    for k, v in kwargs.items():
        name: str = k
        if hasattr(obj, name):
            setattr(obj, name, v)

    return obj
