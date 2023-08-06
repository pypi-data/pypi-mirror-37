#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-19


from json import loads, JSONDecodeError

from gagospecs.v1.base.model import GMDModel
from gagospecs.v1.base.schema import GMDSchema, \
    create_schema


def load_level_and_type_from_gmd(
        gmd_dict: dict
) -> (str, str, dict):
    """
    Load product level and type from a gmd dict object,
    which is from gmd file or url.
    :param gmd_dict: gmd str object
    :return: product level, product type and errors dict
    if there are some errors in gmd_dict
    """
    gmd_schema: GMDSchema = GMDSchema()
    gmd_model, errors = gmd_schema.load(
        gmd_dict,
        False
    )
    if errors:
        return '', '', errors
    gmd_model: GMDModel = gmd_model
    return gmd_model.level, gmd_model.product_type, {}


def load_level_and_type_from_gmd_str(
        gmd_str: str
) -> (str, str, dict):
    """
    Load product level and type from gmd str object
    :param gmd_str:
    :return:
    """
    try:
        gmd_dict: dict = loads(gmd_str)
    except JSONDecodeError:
        return '', '', {
            'GMD格式': 'GMD格式错误'
        }
    return load_level_and_type_from_gmd(gmd_dict)


def load_model_from_gmd(
        gmd_dict: dict
) -> (GMDModel, dict):
    """
    Load a gmd model from a gmd dict object, which is from gmd file or url.
    :param gmd_dict: gmd object dict
    :return: (gmd model, {}) if there is no error in gmd_dict,
    or (None, errors) if there are some errors in a error dict
    """
    gmd_schema: GMDSchema = GMDSchema()
    gmd_model, errors = gmd_schema.load(
        gmd_dict,
        False
    )
    if errors:
        raise ValueError('给定的元数据格式或内容错误，无法加载')

    gmd_model: GMDModel = gmd_model
    real_schema: GMDSchema = create_schema(
        gmd_model.level,
        gmd_model.product_type
    )
    real_model, errors = real_schema.load(
        gmd_dict
    )
    if errors:
        return None, errors
    return real_model, {}
