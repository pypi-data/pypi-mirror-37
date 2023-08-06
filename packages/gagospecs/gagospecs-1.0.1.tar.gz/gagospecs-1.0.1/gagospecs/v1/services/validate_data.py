#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-18


from json import loads, JSONDecodeError

from gagospecs.v1.base.field_mappings import FIELD_MAPPINGS
from gagospecs.v1.base.load_model import \
    load_model_from_gmd
from gagospecs.v1.base.model import GMDModel, \
    DataProperties


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

    gmd_model, errors_dict = load_model_from_gmd(
        gmd_dict
    )

    if errors_dict:
        return errors_dict
    gmd_model: GMDModel = gmd_model
    errors_list: list = gmd_model.validate(
        data_properties
    )
    errors_result_dict = dict()
    for error in errors_list:
        if error in FIELD_MAPPINGS:
            errors_result_dict[
                FIELD_MAPPINGS[error][0] + '/' + error
            ]\
                = '数据值域与元数据不符'
    return errors_result_dict
