#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-26


from gagospecs.v1.base.load_model import \
    load_level_and_type_from_gmd_str
from gagospecs.v1.base.model import DataProperties, GMDProperties
from gagospecs.v1.base.model import create_data_properties, \
    create_gmd_properties


def get_data_properties_from_level_and_type(
        product_level: str,
        product_type: str
) -> DataProperties:
    return create_data_properties(
        product_level,
        product_type
    )


def get_data_properties(
        gmd_str: str,
) -> DataProperties:
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
    return get_data_properties_from_level_and_type(
        product_level,
        product_type
    )


def get_gmd_properties_from_level_and_type(
        product_level: str,
        product_type: str
) -> GMDProperties:
    return create_gmd_properties(
        product_level,
        product_type
    )


def get_gmd_properties(
        gmd_str: str,
) -> GMDProperties:
    product_level, product_type, errors = \
        load_level_and_type_from_gmd_str(
            gmd_str
        )
    if errors:
        return errors
    return get_gmd_properties_from_level_and_type(
        product_level,
        product_type
    )
