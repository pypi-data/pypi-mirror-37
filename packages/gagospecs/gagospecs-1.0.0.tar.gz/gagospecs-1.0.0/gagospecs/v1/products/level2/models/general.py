#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-25


from gagospecs.v1.base.model import GMDModel, \
    DataProperties, \
    GMDProperties, \
    ProductLevelValues


class Level2GMDModel(GMDModel):
    def __init__(self):
        super(Level2GMDModel, self).__init__()
        self.level = ProductLevelValues.Level2


class Level2RasterGMDModel(Level2GMDModel):
    """
    二级栅格产品元数据模型
    """
    def __init__(self):
        super(Level2RasterGMDModel, self).__init__()
        self.columns: int = 0
        self.rows: int = 0
        self.resolution: float = -1

    def _validate(
            self,
            data_properties: DataProperties,
            errors: list
    ):
        if data_properties.columns \
                and self.columns != data_properties.columns:
            errors.append('columns')
        if data_properties.rows \
                and self.rows != data_properties.rows:
            errors.append('rows')
        if data_properties.resolution \
                and self.resolution != data_properties.resolution:
            errors.append('resolution')

    def update(
            self,
            data_properties: DataProperties,
            gmd_properties: GMDProperties
    ):
        super().update(
            data_properties,
            gmd_properties
        )
        if data_properties.columns:
            self.columns = data_properties.columns
        if data_properties.rows:
            self.rows = data_properties.rows
        if data_properties.resolution:
            self.resolution = data_properties.resolution
