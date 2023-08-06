#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-17


from gagospecs.base.base import SpecBase
from gagospecs.v1.base.load_module import create_module


class Converter(SpecBase):
    """
    Gago data product converter base class,
    support automatic conversion of some kind of products,
    for example, ndvi and classification
    """


def create_converter(
        product_level: str,
        product_type: str
) -> Converter or None:
    m = create_module(
        'converters',
        product_level,
        product_type
    )
    if m:
        if hasattr(m, 'main'):
            return m.main()
    return None
