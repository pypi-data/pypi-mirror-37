#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-18


from gagospecs.v1.base.model import DataProperties
from gagospecs.v1.base.validator import create_validator, \
    Validator


def validate_data(
        product_level: str,
        product_type: str,
        data_properties: DataProperties,
        gmd: dict,
) -> list:
    """
    validate if data is correct and if data matches mata data
    :param product_level: product level, a str
    from gagospecs.v1.base.product_level.ProductLevel
    :param product_type: product name, a str
    from gagospeces.v1.base.schema.ProductTypeValues
    :param gmd: gago meta data dict object, from json str
    :param data_properties: properties of data itself(GeoTIFF, GeoJSON...)
    :return:
    """
    validator: Validator = create_validator(
        product_level,
        product_type
    )
    return validator.validate_data(
        data_properties,
        gmd
    )
