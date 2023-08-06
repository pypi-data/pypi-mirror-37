#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-18


from gagospecs.v1.base.model import DataProperties, \
    ProductTypeValues, \
    CoordinateSystemValues, \
    RasterDataTypeValues, \
    GMDProperties, \
    GeoTIFFRasterGMDModel, \
    RasterGMDModel
from gagospecs.v1.products.level2.models.general import Level2RasterGMDModel


class CropClassificationModel(
    GeoTIFFRasterGMDModel,
    RasterGMDModel,
    Level2RasterGMDModel
):
    def __init__(self):
        super(CropClassificationModel, self).__init__()
        self.name = 'CropClassification'
        self.description = 'CropClassification'
        self.product_type = ProductTypeValues.CropClassification
        self.coordinate_system = CoordinateSystemValues.EPSG_4326
        self.data_type = RasterDataTypeValues.Byte
        self.no_data = 255
        self.classification = dict()

    def _validate(
            self,
            data_properties: DataProperties,
            errors: list
    ):
        super()._validate(
            data_properties,
            errors
        )
        if len(self.classification) != \
                len(data_properties.data_value_list) :
            errors.append('classification')
        else:
            for v in data_properties.data_value_list:
                if v not in self.classification:
                    errors.append('classification')
                    break

    def update(
            self,
            data_properties: DataProperties,
            gmd_properties: GMDProperties
    ):
        super().update(
            data_properties,
            gmd_properties
        )
        self.classification = data_properties.classification


def main():
    return CropClassificationModel()


class CropClassificationDataProperties(DataProperties):
    def need_data_value_list(self):
        return True


def main_properties():
    return CropClassificationDataProperties()
