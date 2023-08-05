#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018--10-18


from gagospecs.base.base import SpecBase
from gagospecs.v1.base.load_module import create_module
from gagospecs.v1.base.model import GMDModel


class GMDGenerator(SpecBase):
    """
    Gago meta data(.gmd) generator base class
    """

    def generate(
            self,
            gmd_model: GMDModel
    ) -> str:
        """
        generate gago meta data str from a model
        :param gmd_model:
        :return:
        """
        pass


def create_generator(
        product_level: str,
        product_type: str,
) -> GMDGenerator or None:
    """
    Create a GMD generator
    :param product_level:
    :param product_type:
    :return:
    """
    m = create_module(
        'generators',
        product_level,
        product_type
    )
    if m:
        if hasattr(m, 'main'):
            return m.main()
    return None
