#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-08


import sys
import json
import math
from datetime import datetime

from gagospecs.v1.base.load_module import create_module


FLOAT_THRESHOLD: float = 0.000001


def compare_float(float1: float, float2: float) -> bool:
    return math.fabs(float1 - float2) < FLOAT_THRESHOLD


def _get_min_max(
        extent: list
) -> (float, float, float, float):
    x_min = sys.maxsize
    x_max = -sys.maxsize
    y_min = sys.maxsize
    y_max = -sys.maxsize
    for coordinates in extent:
        x, y = coordinates
        if x < x_min:
            x_min = x
        elif x > x_max:
            x_max = x
        if y < y_min:
            y_min = y
        elif y > y_max:
            y_max = y
    return x_min, y_min, x_max, y_max


class DataProperties:
    """
    用于检验数据本体属性与元数据的集合
    """
    def __init__(self):
        # file type, FileTypeValues
        self.file_type = None
        # RasterDataTypeValues
        self.data_type: str = None
        # no data value
        self.no_data: int = None
        # line count
        self.columns: int = None
        # row count
        self.rows: int = None
        # resolution of image
        self.resolution: float = None
        # CompressionValues, NA, LZW
        self.compression: str = None
        # 坐标偏移
        self.bias: str = None
        # 'EPSG:4326' or 'EPSG:3587'....
        self.coordinate_system: str = None
        # [[x1, y1], [x1, y2], [x2, y2], [x2, y1]]
        self.extent: list = None
        # enum of data values [1, 3, 5, 6]
        # for crop classification like product
        self.data_value_list: list = None
        # min value, for continuous product
        self.data_min: int = None
        # max value, for continuous product
        self.data_max: int = None
        # GeometryTypeValues, for Vector Product
        self.geometry_type: str = None
        # Min tile level
        self.min_tile_level: int = None
        # Max tile level
        self.max_tile_level: int = None
        # classification information
        self.classification: dict = None

    def need_data_value_list(self) -> bool:
        return False


class GMDProperties:
    def __init__(self):
        # product name
        self.name: str = None
        # product description
        self.description: str = None
        # QC, will append to QC
        self.qc: str = None
        # Production datetime
        self.production_datetime: datetime = None
        # Producer, will append to producer
        self.producer: str = None


class GMDModel:
    def __init__(self):
        self.version: str = '1.0'
        self.name: str = ''
        self.description: str = ''
        self.level: str = ''
        self.category: str = ''
        self.product_type: str = ''
        self.file_type: str = ''
        self.production_datetime: datetime = None
        self.producer: str = ''
        self.qc: str = ''

    def validate(
            self,
            data_properties: DataProperties
    ) -> list:
        validation_errors: list = []
        self._validate(
            data_properties,
            validation_errors
        )
        return validation_errors

    def _validate(
            self,
            data_properties: DataProperties,
            errors: list
    ):
        if self.file_type != data_properties.file_type:
            errors.append('file_type')

    def update(
            self,
            data_properties: DataProperties,
            gmd_properties: GMDProperties
    ):
        if gmd_properties.name:
            self.name = gmd_properties.name
        if gmd_properties.description:
            self.description = gmd_properties.description
        if gmd_properties.production_datetime:
            self.production_datetime = gmd_properties.production_datetime
        if gmd_properties.producer:
            producer_list = self.producer.split('#') \
                if self.producer \
                else list()
            producer_list.append(gmd_properties.producer)
            self.producer = '#'.join(producer_list)
        if gmd_properties.qc:
            qc_list = self.qc.split('#') \
                if self.qc \
                else list()
            qc_list.append(gmd_properties.qc)
            self.qc = '#'.join(qc_list)

    def copy_from(
            self,
            gmd_model
    ):
        self.producer = getattr(gmd_model, 'producer', self.producer)
        self.qc = getattr(gmd_model, 'qc', self.qc)


class SpatialGMDModel(GMDModel):
    def __init__(self):
        super().__init__()
        self.coordinate_system: str = ''
        self.extent: str = ''
        self.bias: str = 'NA'

    def _validate(
            self,
            data_properties: DataProperties,
            errors: list
    ):
        super()._validate(
            data_properties,
            errors
        )
        if self.coordinate_system != data_properties.coordinate_system:
            errors.append('coordinate_system')
        try:
            extent_value = json.loads(self.extent)
            x1_min, y1_min, x1_max, y1_max = _get_min_max(extent_value)
            x2_min, y2_min, x2_max, y2_max = _get_min_max(data_properties.extent)
            if not compare_float(x1_min, x2_min) \
                    or not compare_float(y1_min, y2_min) \
                    or not compare_float(x1_max, x2_max) \
                    or not compare_float(y1_max, y2_max):
                errors.append('extent')
        except json.JSONDecodeError:
            errors.append('extent')

    def update(
            self,
            data_properties: DataProperties,
            gmd_properties: GMDProperties
    ):
        super().update(
            data_properties,
            gmd_properties
        )
        if data_properties.coordinate_system:
            self.coordinate_system = \
                data_properties.coordinate_system
        if data_properties.extent:
            self.extent = data_properties.extent
        if data_properties.bias:
            self.bias = data_properties.bias

    def copy_from(
            self,
            gmd_model: GMDModel
    ):
        super().copy_from(gmd_model)
        self.coordinate_system = getattr(
            gmd_model,
            'coordinate_system',
            self.coordinate_system
        )
        self.extent = getattr(
            gmd_model,
            'extent',
            self.extent
        )
        self.bias = getattr(
            gmd_model,
            'bias',
            self.bias
        )


class RasterGMDModel(SpatialGMDModel):
    def __init__(self):
        super().__init__()
        self.category = CategoryValues.Raster
        self.no_data: int = -1
        self.data_type: str = None

    def _validate(
            self,
            data_properties: DataProperties,
            errors: list
    ):
        super()._validate(
            data_properties,
            errors
        )
        if self.no_data != data_properties.no_data:
            errors.append('no_data')
        if self.data_type != data_properties.data_type:
            errors.append('data_type')

    def update(
            self,
            data_properties: DataProperties,
            gmd_properties: GMDProperties
    ):
        super().update(
            data_properties,
            gmd_properties
        )
        if data_properties.no_data:
            self.no_data = data_properties.no_data
        if data_properties.data_type:
            self.data_type = data_properties.data_type

    def copy_from(
            self,
            gmd_model: GMDModel
    ):
        super().copy_from(
            gmd_model
        )
        self.no_data = getattr(
            gmd_model,
            'no_data',
            self.no_data
        )
        self.data_type = getattr(
            gmd_model,
            'data_type',
            self.data_type
        )


class FloatRasterGMDModel(RasterGMDModel):
    def __init__(self):
        super().__init__()
        self.scale_factor: float = 1.0
        self.linear_factor: float = 1.0

    def copy_from(
            self,
            gmd_model: GMDModel
    ):
        super().copy_from(gmd_model)
        self.scale_factor = getattr(
            gmd_model,
            'scale_factor',
            self.scale_factor
        )
        self.linear_factor = getattr(
            gmd_model,
            'linear_factor',
            self.linear_factor
        )


class GeoTIFFRasterGMDModel(GMDModel):
    def __init__(self):
        super().__init__()
        self.file_type: str = FileTypeValues.GeoTIFF
        self.compression: str = CompressionValues.LZW

    def _validate(
            self,
            data_properties: DataProperties,
            errors: list
    ):
        super()._validate(
            data_properties,
            errors
        )
        if self.compression != data_properties.compression:
            errors.append('compression')

    def update(
            self,
            data_properties: DataProperties,
            gmd_properties: GMDProperties
    ):
        super().update(
            data_properties,
            gmd_properties
        )
        if data_properties.compression:
            self.compression = data_properties.compression


def create_model(
        product_level: str,
        product_type: str
) -> GMDModel or None:
    """
    Create a GMD model
    :param product_level: product level,
    which laid in gagospecs.v1.base.product_level.ProductLevel class
    :param product_type: product name
    :return: requested GMD model object
    """
    m = create_module(
        'models',
        product_level,
        product_type
    )
    if m:
        if hasattr(m, 'main'):
            return getattr(m, 'main')()
    return None


def create_data_properties(
        product_level: str,
        product_type: str
) -> DataProperties or None:
    """
    Get DataProperies object needed
    for the specified product
    :param product_level:
    :param product_type:
    :return:
    """
    m = create_module(
        'models',
        product_level,
        product_type
    )
    if m:
        if hasattr(m, 'main_properties'):
            return m.main_properties()
    return DataProperties()


def create_gmd_properties(
        product_level: str,
        product_type: str
) -> GMDProperties or None:
    """
    Get GMDProperties object needed
    for the specified product
    :param product_level:
    :param product_type:
    :return:
    """
    m = create_module(
        'models',
        product_level,
        product_type
    )
    if m:
        if hasattr(m, 'main_gmd_properties'):
            return m.main_gmd_properties()
    return GMDProperties()


class ValuesBase:
    """
    值域表基类
    """
    @classmethod
    def get_value_set(cls) -> set:
        values_set: set = set()
        for k, v in cls.__dict__.items():
            key: str = k
            value: str = v
            if (not key.startswith('__')
                and value not in values_set):
                values_set.add(value)
        return values_set


class ProductLevelValues(ValuesBase):
    """
    Product level
    """
    Level1 = 'level1'
    Level2 = 'level2'
    Level3 = 'level3'


class CategoryValues(ValuesBase):
    """
    产品分类值域表
    """
    Raster = 'Raster'
    Vector = 'Vector'
    Attribute = 'Attribute'


class ProductTypeValues(ValuesBase):
    """
    产品类型值域表
    """
    BaseMap = 'BaseMap'
    NDVI = 'NDVI'
    CropClassification = 'CropClassification'
    DisasterAssessment = 'DisasterAssessment'
    PDSI = 'PDSI'
    SMAP = 'SMAP'
    AdministrativeArea = 'AdministrativeArea'
    LandBlock = 'LandBlock'
    Statistics = 'Statistics'
    WeatherLive = 'WeatherLive'
    WeatherHistory = 'WeatherHistory'
    WeatherForecast = 'WeatherForecast'


class WeatherProductTypeValues(ValuesBase):
    """
    气象产品类型值域表
    """
    NA = 'NA'
    WeatherPhenomenon = 'WeatherPhenomenon'
    Temperature = 'Temperature'
    Moisture = 'Moisture'
    Precipitation = 'Precipitation'
    WindDirection = 'WindDirection'
    WindPower = 'WindPower'
    Pressure = 'Pressure'
    AirQuality = 'AirQuality'


class FileTypeValues(ValuesBase):
    """
    文件类型值域表
    """
    GeoTIFF = 'GeoTIFF'
    JPEG = 'JPEG'
    PNG = 'PNG'
    LERC = 'LERC'
    BIP = 'BIP'
    GeoJSON = 'GeoJSON'
    SHP = 'SHP'
    JSON = 'JSON'


class CoordinateSystemValues(ValuesBase):
    """
    坐标系统值域表
    """
    EPSG_3857 = 'EPSG:3857'
    EPSG_4326 = 'EPSG:4326'


class BiasValues(ValuesBase):
    """
    坐标系偏移值域表
    """
    NA = 'NA'
    GCJ_02 = 'GCJ-02'


class RasterDataTypeValues(ValuesBase):
    """
    栅格像元数据类型值域表
    """
    Byte = 'Byte'
    UInt16 = 'UInt16'
    UInt32 = 'UInt32'


class CompressionValues(ValuesBase):
    """
    栅格数据压缩方法值域表
    """
    NA = 'NA'
    LZW = 'LZW'


class GeometryTypeValues(ValuesBase):
    """
    几何类型值域表
    """
    Point = 'Point'
    Polyline = 'Polyline'
    Polygon = 'Polygon'
