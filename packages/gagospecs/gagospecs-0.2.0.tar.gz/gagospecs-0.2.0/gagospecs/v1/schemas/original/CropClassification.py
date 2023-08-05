#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-18


from marshmallow import validates, \
    ValidationError, \
    post_load
from marshmallow.fields import Dict

from gagospecs.v1.base.schema import RasterGMDSchema, \
    GeoTIFFGMDSchema
from gagospecs.v1 import ProductTypeValues, \
    FileTypeValues, \
    RasterDataTypeValues, \
    CompressionValues
from gagospecs.v1.models.original.CropClassification \
    import CropClassificationModel
from gagospecs.v1.base.schema import post_load_object


class CropClassificationSchema(RasterGMDSchema, GeoTIFFGMDSchema):
    """
    Crop classification schema
    """
    classification = Dict(required=True)

    @validates('file_type')
    def validate_file_type(self, value):
        if value != FileTypeValues.GeoTIFF:
            raise ValidationError('作物分类栅格产品必须为GeoTIFF格式')

    @validates('product_type')
    def validate_product_type(self, value):
        if value != ProductTypeValues.CropClassification:
            raise ValidationError('作物分类栅格产品的product_type'
                                  '字段必须为"CropClassification"')

    @validates('data_type')
    def validate_data_type(self, value):
        if value != RasterDataTypeValues.Byte:
            raise ValidationError('作物分类栅格产品data_type字段必须为"Byte"')

    @validates('no_data')
    def validate_no_data(self, value):
        if value != 255:
            raise ValidationError('作物分类栅格产品no_data字段必须为"255"')

    @validates('compression')
    def validate_linear_factor(self, value):
        if value != CompressionValues.LZW:
            raise ValidationError('作物分类栅格产品产品compression字段必须为"LZW"')

    @validates('classification')
    def validate_classification(self, value):
        value: dict = value
        for k, v in value.items():
            if not isinstance(k, int) or k < 0 or k > 254:
                raise ValidationError('classification分类值错误')
            if not isinstance(v, str):
                raise ValidationError('classification分类值错误')

    @post_load
    def make_object(self, data: dict):
        return post_load_object(CropClassificationModel(), **data)


def main():
    return CropClassificationSchema()
