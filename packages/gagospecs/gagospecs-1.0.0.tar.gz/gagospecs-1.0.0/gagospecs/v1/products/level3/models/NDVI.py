#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-25


from gagospecs.v1.base.model import FloatRasterGMDModel, \
    RasterDataTypeValues, \
    FileTypeValues, \
    CoordinateSystemValues, \
    ProductTypeValues
from gagospecs.v1.products.level3.models.general import Level3RasterModel


class NDVIModel(
    FloatRasterGMDModel,
    Level3RasterModel
):
    def __init__(self):
        super(NDVIModel, self).__init__()
        self.name = 'NDVI'
        self.description = 'NDVI'
        self.product_type = ProductTypeValues.NDVI
        self.coordinate_system = CoordinateSystemValues.EPSG_4326
        self.data_type = RasterDataTypeValues.Byte
        self.no_data = 255
        self.file_type = FileTypeValues.LERC
        self.linear_factor = -127
        self.scale_factor = 0.0078125


def main():
    return NDVIModel()
