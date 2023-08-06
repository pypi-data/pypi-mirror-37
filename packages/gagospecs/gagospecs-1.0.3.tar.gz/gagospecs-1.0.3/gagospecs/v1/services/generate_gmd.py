#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-25


import json

from gagospecs.v1.base.load_model import load_model_from_gmd
from gagospecs.v1.base.model import DataProperties, \
    GMDProperties, \
    GMDModel, \
    create_model
from gagospecs.v1.base.schema import GMDSchema, \
    create_schema
from gagospecs.v1.services.validate_gmd import validate_gmd


def generate_from_data(
        product_level: str,
        product_type: str,
        data_properties: DataProperties,
        gmd_properties: GMDProperties
) -> (GMDModel, str, dict):
    """
    Generate a gmd model and str from data
    properties and gmd properties
    :param product_level:
    :param product_type:
    :param data_properties: Properties from data itself
    :param gmd_properties: Properties extra for gmd, name, description, etc
    :return: GMDModel, serialized GMDModel and errors
    """
    gmd_model: GMDModel = create_model(
        product_level,
        product_type
    )
    if gmd_model is None:
        return None, None, {
            'gmd': '指定产品级别或类型错误，无法创建元数据模型'
        }
    gmd_model.update(
        data_properties,
        gmd_properties
    )
    schema: GMDSchema = create_schema(
        product_level,
        product_type
    )
    gmd_str, errors = schema.dumps(gmd_model)
    if errors:
        return None, None, errors
    errors: dict = validate_gmd(
        gmd_str
    )
    if errors:
        return None, None, errors
    return \
        gmd_model, \
        gmd_str.encode('latin-1').decode('unicode_escape'), \
        {}


def generate_from_gmd(
        src_gmd: str or dict or GMDModel,
        dst_product_level: str,
        data_properties: DataProperties,
        gmd_properties: GMDProperties
) -> (GMDModel, str, dict):
    """
    Generate a gmd model from given source gmd model
    :param src_gmd:
    :param dst_product_level:
    :param data_properties:
    :param gmd_properties:
    :return: A tuple include GMDModel, serialized GMDModel and error dict
    """

    src_gmd_dict: dict = None
    if isinstance(src_gmd, str):
        try:
            src_gmd_dict = json.loads(
                src_gmd
            )
        except json.JSONDecodeError:
            return None, None, {
                'gmd内容': 'Gago Meta Data 内容错误'
            }

    if isinstance(src_gmd, dict):
        src_gmd_dict = src_gmd

    if src_gmd_dict:
        src_gmd_model, errors = \
            load_model_from_gmd(
                src_gmd_dict
            )
        if errors:
            return None, None, errors
    elif isinstance(src_gmd, GMDModel):
        src_gmd_model: GMDModel = src_gmd
    else:
        raise ValueError(
            'src_gmd is not str, dict or GMDModel'
        )

    product_type: str = src_gmd_model.product_type

    dst_gmd_model: GMDModel = create_model(
        dst_product_level,
        product_type
    )
    if not dst_gmd_model:
        return None, None, {
            'gmd内容': '无法根据GMD创建指定的元数据对象'
        }

    dst_gmd_model.copy_from(src_gmd_model)
    dst_gmd_model.update(
        data_properties,
        gmd_properties
    )

    dst_schema: GMDSchema = create_schema(
        dst_product_level,
        product_type
    )
    if not dst_schema:
        return None, None, {
            'gmd错误': '无法根据GMD验证指定的元数据对象'
        }
    dst_gmd_str, errors = dst_schema.dumps(dst_gmd_model)
    if errors:
        return None, None, errors
    errors: dict = validate_gmd(
        dst_gmd_str
    )
    if errors:
        return None, None, errors
    return \
        dst_gmd_model, \
        dst_gmd_str.encode('latin-1').decode('unicode_escape'), \
        {}
