#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-25


from gagospecs.v1.base.model import GMDModel, \
    DataProperties, \
    GMDProperties, \
    ProductLevelValues


class Level3Model(GMDModel):
    def __init__(self):
        super(Level3Model, self).__init__()
        self.level = ProductLevelValues.Level3


class Level3RasterModel(Level3Model):
    """
    三级栅格产品GMD模型
    """
    def __init__(self):
        super(Level3RasterModel, self).__init__()
        self.min_tile_level = -1
        self.max_tile_level = -1

    def _validate(
            self,
            data_properties: DataProperties,
            errors: list
    ):
        super()._validate(
            data_properties,
            errors
        )
        if self.min_tile_level != \
                data_properties.min_tile_level:
            errors.append('min_tile_level')
        if self.max_tile_level != \
                data_properties.max_tile_level:
            errors.append('max_tile_level')

    def update(
            self,
            data_properties: DataProperties,
            gmd_properties: GMDProperties
    ):
        super().update(
            data_properties,
            gmd_properties
        )
        if data_properties.min_tile_level is not None:
            self.min_tile_level = \
                data_properties.min_tile_level
        if data_properties.max_tile_level is not None:
            self.max_tile_level = \
                data_properties.max_tile_level
