#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-08


from datetime import datetime

from gagospecs.v1.base.load_module import create_module


class DataProperties:
    """
    用于检验数据本体属性与元数据的集合
    """
    def __init__(self):
        # file type, FileTypeValues
        self.file_type = ''
        # RasterDataTypeValues
        self.data_type: str = ''
        # no data value
        self.no_data: int = -1
        # line count
        self.lines: int = -1
        # row count
        self.rows: int = -1
        # resolution of image
        self.resolution: float = -1
        # CompressionValues, NA, LZW
        self.compression: str = ''
        # 4326 3587....
        self.coordinate_system: float = -1.0
        # [[x1, y1], [x1, y2], [x2, y2], [x2, y1]]
        self.extent: str = ''
        # enum of data values [1, 3, 5, 6]
        # for crop classification like product
        self.data_value_list: list = []
        # min value, for continuous product
        self.data_min: int = None
        # max value, for continuous product
        self.data_max: int = None
        # GeometryTypeValues, for Vector Product
        self.geometry_type: str = ''

    def need_data_value_list(self) -> bool:
        return False

    def need_data_min(self) -> bool:
        return False

    def need_data_max(self) -> bool:
        return False


class GMDModel:
    def __init__(self):
        self.version: str = '1.0'
        self.name: str = ''
        self.description: str = ''
        self.level: str = ''
        self.category: str = ''
        self.product_type: str = ''
        self.file_type: str = ''
        self.production_date: datetime = None
        self.producer: str = ''
        self.qc: str = ''

    def validate(
            self,
            data_properties: DataProperties
    ) -> (bool, list):
        validation_errors: list = []
        if self.file_type != data_properties.file_type:
            validation_errors.append('file_type')
        self._validate(
            data_properties,
            validation_errors
        )
        return len(validation_errors) == 0, validation_errors

    def _validate(
            self,
            data_properties: DataProperties,
            errors: list
    ):
        pass


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
        if self.extent != data_properties.extent:
            errors.append('extent')


class RasterGMDModel(SpatialGMDModel):
    def __init__(self):
        super().__init__()
        self.category = CategoryValues.Raster
        self.no_data: int = -1
        self.data_type: str = None
        self.lines: int = 0
        self.rows: int = 0
        self.resolution: float = -1

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
        if self.lines != data_properties.lines:
            errors.append('lines')
        if self.rows != data_properties.rows:
            errors.append('rows')
        if self.resolution != data_properties.resolution:
            errors.append('resolution')


class FloatRasterGMDModel(RasterGMDModel):
    def __init__(self):
        super().__init__()
        self.scale_factor: float = 1.0
        self.linear_factor: float = 1.0


class GeoTIFFRasterGMDModel(GMDModel):
    def __init__(self):
        self.compression: str = None
        super().__init__()

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
    Original = 'original'
    Publishable = 'publishable'
    deliverable = 'deliverable'


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
