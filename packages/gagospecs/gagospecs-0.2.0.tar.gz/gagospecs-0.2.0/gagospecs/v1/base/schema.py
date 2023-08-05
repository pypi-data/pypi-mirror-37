#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-07


import json

from marshmallow import Schema, \
    validates, \
    ValidationError, \
    post_load
from marshmallow.fields import String, \
    DateTime, \
    Integer, \
    Float

from gagospecs.v1 import \
    CoordinateSystemValues, \
    CompressionValues, \
    GeometryTypeValues
from gagospecs.v1.base.load_module import \
    create_module
from gagospecs.v1.base.model import \
    GMDModel, \
    CategoryValues, \
    BiasValues


def post_load_object(obj, **kwargs):
    for k, v in kwargs.items():
        name: str = k
        if hasattr(obj, name):
            setattr(obj, name, v)

    return obj


class GMDSchema(Schema):
    """
    GMD佳格元数据模式
    """
    version = String(default='1.0', required=True)
    name = String(required=True, allow_none=False)
    description = String(required=True)
    level = String(required=True)
    category = String(required=True)
    product_type = String(required=True)
    file_type = String(required=True)
    production_date = DateTime(required=True, format='%Y-%m-%dT%H:%M:%S%z')
    producer = String(required=False)
    qc = String(required=False)

    @validates('version')
    def validate_version(self, value):
        if value != '1.0':
            raise ValidationError('version字段必须为1.0')

    @post_load
    def make_object(self, data: dict):
        return post_load_object(GMDModel(), **data)


class SpatialGMDSchema(GMDSchema):
    """
    空间数据产品GMD模式
    """
    coordinate_system = String(required=True, allow_none=False)
    extent = String(required=True, allow_none=False)
    bias = String(required=True, allow_none=False)

    @validates('coordinate_system')
    def validate_coordinate_system(self, value):
        if value not in CoordinateSystemValues.get_value_set():
            raise ValidationError(
                'coordinate_system字段必须为"EPSG:3857"或"EPSG:4326"'
            )

    @validates('extent')
    def validate_extent(self, value):
        try:
            extent_value: dict = json.loads(value)
            if not isinstance(extent_value, list):
                raise ValidationError('extent字段必须为坐标数组')
            if len(extent_value) != 4:
                raise ValidationError('extent字段坐标数组必须为4对坐标值')
            for coordinates in extent_value:
                if not isinstance(coordinates, list) or \
                                len(coordinates) != 2:
                    raise ValidationError('extent字段坐标必须为坐标对')
        except json.JSONDecodeError:
            raise ValidationError('extent字段必须为合法JSON字符串')

    @validates('bias')
    def validate_bias(self, value):
        if value not in BiasValues.get_value_set():
            raise ValidationError('bias字段必须为"NA"或"CGJ-02"')


class RasterGMDSchema(SpatialGMDSchema):
    """
    栅格数据GMD头文件模式
    """
    no_data = Integer(required=True, allow_none=False)
    data_type = String(required=True, allow_none=False)
    lines = Integer(required=True, allow_none=False)
    rows = Integer(required=True, allow_none=False)
    resolution = Float(required=True, allow_none=False)

    @validates('category')
    def validate_category(self, value):
        if value != CategoryValues.Raster:
            raise ValidationError('category字段值必须为Raster')

    @validates('lines')
    def validate_lines(self, value):
        if value <= 0:
            raise ValidationError('lines字段必须大于0')

    @validates('rows')
    def validate_rows(self, value):
        if value <= 0:
            raise ValidationError('rows字段必须大于0')

    @validates('resolution')
    def validate_resolution(self, value):
        if value <= 0:
            raise ValidationError('resolution字段必须大于0')


class FloatRasterGMDSchema(RasterGMDSchema):
    """
    浮点型栅格数据产品GMD头文件模式
    """
    scale_factor = Float(required=True)
    linear_factor = Float(required=True)

    @validates('scale_factor')
    def validate_scale_factor(self, value):
        if value <= 0:
            raise ValidationError('scale_factor字段必须大于0')


class GeoTIFFGMDSchema(Schema):
    """
    GeoTIFF头文件模式
    """
    compression = String(required=True)

    @validates('compression')
    def validate_compression(self, value):
        if value not in CompressionValues.get_value_set():
            raise ValidationError('compression字段只能为"NA"或"LZW"')


class VectorGMDSchema(SpatialGMDSchema):
    """
    矢量数据GMD头文件模式
    """
    geometry_type = String(required=True)

    @validates('geometry_type')
    def validate_geometry_type(self, value):
        if value not in GeometryTypeValues.get_value_set():
            raise ValidationError(
                'geometry_type字段只能为"Point", "Polyline"或"Polygon"'
            )


def create_schema(
        product_level: str,
        product_type: str,
) -> GMDSchema or None:
    """
    create a schema object
    :param product_level:
    :param product_type:
    :return:
    """
    m = create_module(
        'schemas',
        product_level,
        product_type
    )
    if m:
        if hasattr(m, 'main'):
            return m.main()
    return None
