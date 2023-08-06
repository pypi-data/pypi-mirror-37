#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 


from marshmallow import validates, \
    ValidationError, \
    post_load
from marshmallow.fields import Dict, \
    Integer, \
    String

from gagospecs.v1 import ProductTypeValues, \
    FileTypeValues, \
    RasterDataTypeValues, \
    CompressionValues
from gagospecs.v1.base.schema import RasterGMDSchema
from gagospecs.v1.base.schema import post_load_object
from gagospecs.v1.products.level3.models.CropClassification \
    import CropClassificationModel
from gagospecs.v1.products.level3.schemas.general import Level3RasterSchema


class CropClassificationSchema(
    RasterGMDSchema,
    Level3RasterSchema
):
    """
    Crop classification schema
    """
    classification = Dict(keys=Integer(), values=String(), required=True)

    @validates('file_type')
    def validate_file_type(self, value):
        if value != FileTypeValues.LERC:
            raise ValidationError('作物分类栅格产品必须为LERC格式')

    @validates('product_type')
    def validate_product_type(self, value):
        if value != ProductTypeValues.CropClassification:
            raise ValidationError(
                '作物分类栅格产品的product_type字段必须为"CropClassification"'
            )

    @validates('data_type')
    def validate_data_type(self, value):
        if value != RasterDataTypeValues.Byte:
            raise ValidationError('作物分类栅格产品data_type字段必须为"Byte"')

    @validates('no_data')
    def validate_no_data(self, value):
        if value != 255:
            raise ValidationError('作物分类栅格产品no_data字段必须为"255"')

    @validates('classification')
    def validate_classification(self, value):
        value: dict = value
        for k, v in value.items():
            try:
                k_int: int = int(k)
            except ValueError:
                raise ValidationError('classification分类值中像元值不为整型')
            if k_int < 0 or k_int > 254:
                raise ValidationError('classification分类值中像元值不合法，应为0到254之间（含）')
            if not isinstance(v, str):
                raise ValidationError('classification分类值作物名称错误')

    @post_load
    def make_object(self, data: dict):
        return post_load_object(CropClassificationModel(), **data)


def main():
    return CropClassificationSchema()