#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-18


from json import loads, JSONDecodeError

from gagospecs.v1.base.load_model import \
    load_level_and_type_from_gmd
from gagospecs.v1.base.schema import GMDSchema, \
    create_schema


def validate_gmd(
        gmd_str: str
) -> dict:
    """
    Validate a gmd dict object loaded from a gmd file or url
    :param gmd_str:
    :return: errors. if it is empty, the gmd is right
    """
    try:
        gmd_dict: dict = loads(gmd_str)
    except JSONDecodeError:
        return {'GMD内容': 'Gago Meta Data 内容错误'}

    product_level, product_type, errors = \
        load_level_and_type_from_gmd(
            gmd_dict
        )
    if errors:
        return errors

    schema: GMDSchema = create_schema(
        product_level,
        product_type
    )
    if not schema:
        return {
            'GMD内容':
                '"level"和"product_type字段可能有误，'
                '无法加载数据规格"'
        }

    return schema.validate(gmd_dict)
