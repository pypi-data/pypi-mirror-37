#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-18


from gagospecs.v1.base.schema import CategoryValues, \
    CoordinateSystemValues, \
    RasterDataTypeValues, \
    FileTypeValues, \
    CompressionValues, \
    ProductTypeValues
from gagospecs.v1.base.model import GeoTIFFRasterGMDModel, \
    RasterGMDModel


class CropClassificationModel(RasterGMDModel, GeoTIFFRasterGMDModel):
    def __init__(self):
        super(CropClassificationModel, self).__init__()
        self.name = 'CropClassification'
        self.description = 'CropClassification'
        self.category = CategoryValues.Raster
        self.coordinate_system = CoordinateSystemValues.EPSG_4326
        self.data_type = RasterDataTypeValues.Byte
        self.no_data = 255
        self.file_type = FileTypeValues.GeoTIFF
        self.compression = CompressionValues.LZW
        self.product_type = ProductTypeValues.CropClassification
        self.classification = dict()


def main():
    return CropClassificationModel()
