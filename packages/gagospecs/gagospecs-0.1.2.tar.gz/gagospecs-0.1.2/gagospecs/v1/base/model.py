#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-08


from datetime import datetime

from gagospecs.v1.base.load_module import create_module
from gagospecs.v1.base.schema import CategoryValues


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
