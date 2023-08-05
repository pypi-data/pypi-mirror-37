#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-18


from gagospecs.v1.base.validator import create_validator, Validator


def validate_gmd(
        product_level: str,
        product_type: str,
        gmd: dict
) -> dict:
    """
    Validate a gmd dict object loaded from a gmd file or url
    :param product_level: product level, a str
    from gagospecs.v1.base.product_level.ProductLevel
    :param product_type: product name, a str
    from gagospeces.v1.base.schema.ProductTypeValues
    :param gmd:
    :return: errors. if it is empty, the gmd is right
    """

    validator: Validator = create_validator(
        product_level,
        product_type
    )

    return validator.validate(
        product_level,
        product_type,
        gmd
    )
