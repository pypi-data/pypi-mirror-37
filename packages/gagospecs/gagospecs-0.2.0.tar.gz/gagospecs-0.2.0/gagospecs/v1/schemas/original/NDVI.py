#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 018-10-17


from marshmallow import \
    ValidationError, \
    validates, \
    post_load

from gagospecs.v1.base.schema import \
    FloatRasterGMDSchema, \
    GeoTIFFGMDSchema
from gagospecs.v1 import ProductLevelValues, \
    ProductTypeValues, \
    FileTypeValues, \
    RasterDataTypeValues, \
    CompressionValues
from gagospecs.v1.models.original.NDVI import NDVIModel
from gagospecs.v1.base.schema import post_load_object


class NDVISchema(FloatRasterGMDSchema, GeoTIFFGMDSchema):
    @validates('level')
    def validate_level(self, value):
        if value != ProductLevelValues.Original:
            raise ValidationError('NDVI栅格产品level字段必须为original')

    @validates('file_type')
    def validate_file_type(self, value):
        if value != FileTypeValues.GeoTIFF:
            raise ValidationError('NDVI栅格产品file_type字段必须为"GeoTIFF"')

    @validates('product_type')
    def validate_product_type(self, value):
        if value != ProductTypeValues.NDVI:
            raise ValidationError('NDVI栅格产品的product_type字段必须为"NDVI"')

    @validates('data_type')
    def validate_data_type(self, value):
        if value != RasterDataTypeValues.Byte:
            raise ValidationError('NDVI栅格产品data_type字段必须为"Byte"')

    @validates('no_data')
    def validate_no_data(self, value):
        if value != 255:
            raise ValidationError('NDVI栅格产品no_data字段必须为"255"')

    @validates('scale_factor')
    def validate_scale_factor(self, value):
        if value != 0.0078125:
            raise ValidationError('NDVI栅格产品scale_factor字段必须为"0.0078125"')

    @validates('linear_factor')
    def validate_linear_factor(self, value):
        if value != -127:
            raise ValidationError('NDVI栅格产品linear_factor字段必须为"-127"')

    @validates('compression')
    def validate_compression(self, value):
        if value != CompressionValues.LZW:
            raise ValidationError('NDVI栅格产品compression字段必须为"LZW"')

    @post_load
    def make_object(self, data: dict):
        return post_load_object(NDVIModel(), **data)


def main():
    return NDVISchema()
