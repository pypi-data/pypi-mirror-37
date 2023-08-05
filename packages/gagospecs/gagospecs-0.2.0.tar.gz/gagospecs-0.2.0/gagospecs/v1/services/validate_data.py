#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-18


from json import loads, JSONDecodeError

from gagospecs.v1.base.load_model import \
    load_level_and_type_from_gmd, \
    load_level_and_type_from_gmd_str
from gagospecs.v1.base.model import DataProperties
from gagospecs.v1.base.model import create_data_properties
from gagospecs.v1.base.validator import create_validator, \
    Validator


def get_data_properties(
        gmd_str: str,
) -> dict:
    """
    get a DataProperties object from a gmd str
    :param gmd_str: gmd str from gmd file or url
    :return: DataProperties object
    """
    product_level, product_type, errors = \
        load_level_and_type_from_gmd_str(
            gmd_str
        )
    if errors:
        return errors
    return create_data_properties(
        product_level,
        product_type
    )


def validate_data(
        data_properties: DataProperties,
        gmd_str: str,
) -> dict:
    """
    validate if data is correct and if data matches mata data
    :param gmd_str: gago meta data dict object, from json str
    :param data_properties: properties of data itself(GeoTIFF, GeoJSON...)
    :return:
    """
    try:
        gmd_dict: dict = loads(gmd_str)
    except JSONDecodeError:
        return {'gmd内容': 'Gago Meta Data 内容错误'}

    product_level, product_type, errors = \
        load_level_and_type_from_gmd(
            gmd_dict
        )
    if errors:
        return errors
    validator: Validator = create_validator(
        product_level,
        product_type
    )
    return validator.validate_data(
        data_properties,
        gmd_dict
    )
