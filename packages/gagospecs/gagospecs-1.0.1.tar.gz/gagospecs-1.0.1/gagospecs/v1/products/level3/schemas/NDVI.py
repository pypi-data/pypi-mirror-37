#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-25


from marshmallow import validates, \
    ValidationError, \
    post_load

from gagospecs.v1.base.model import FileTypeValues, \
    ProductTypeValues, \
    RasterDataTypeValues
from gagospecs.v1.base.schema import FloatRasterGMDSchema
from gagospecs.v1.base.schema import post_load_object
from gagospecs.v1.products.level3.models.NDVI import NDVIModel
from gagospecs.v1.products.level3.schemas.general import Level3RasterSchema


class NDVISchema(
    FloatRasterGMDSchema,
    Level3RasterSchema
):
    @validates('file_type')
    def validate_file_type(self, value):
        if value != FileTypeValues.LERC:
            raise ValidationError('三级NDVI产品file_type字段必须为LERC')

    @validates('product_type')
    def validate_product_type(self, value):
        if value != ProductTypeValues.NDVI:
            raise ValidationError('三级NDVI栅格产品的product_type字段必须为"NDVI"')

    @validates('data_type')
    def validate_data_type(self, value):
        if value != RasterDataTypeValues.Byte:
            raise ValidationError('三级NDVI栅格产品data_type字段必须为"Byte"')

    @validates('no_data')
    def validate_no_data(self, value):
        if value != 255:
            raise ValidationError('三级NDVI栅格产品no_data字段必须为"255"')

    @validates('scale_factor')
    def validate_scale_factor(self, value):
        if value != 0.0078125:
            raise ValidationError('三级NDVI栅格产品scale_factor字段必须为"0.0078125"')

    @validates('linear_factor')
    def validate_linear_factor(self, value):
        if value != -127:
            raise ValidationError('三级NDVI栅格产品linear_factor字段必须为"-127"')

    @post_load
    def make_object(self, data: dict):
        return post_load_object(NDVIModel(), **data)


def main():
    return NDVISchema()
